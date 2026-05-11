# =========================
# IMPORTS
# =========================

from faster_whisper import WhisperModel
from pydub import AudioSegment

import math
import os
import re
import time


# =========================
# MODEL INIT (ОДИН РАЗ)
# =========================

model = WhisperModel("large-v3", device="cuda", compute_type="float16")


# =========================
# NORMALIZE
# =========================


def normalize_audio(file_path):
    """
    Приводит любой аудиофайл к WAV 16kHz mono.
    Важно: вызываем один раз на весь входной файл.
    """

    try:
        audio = AudioSegment.from_file(file_path)
    except Exception as e:
        raise Exception(f"Ошибка чтения аудио: {e}")

    audio = audio.set_frame_rate(16000).set_channels(1)

    wav_path = file_path + "_normalized.wav"
    audio.export(wav_path, format="wav")

    return wav_path


# =========================
# SPLIT
# =========================


def split_audio(file_path, chunk_minutes=10):
    """
    Делит уже нормализованный WAV на чанки.
    Повторно не нормализует.
    """

    audio = AudioSegment.from_file(file_path)

    chunk_length_ms = chunk_minutes * 60 * 1000
    total_length_ms = len(audio)
    total_chunks = math.ceil(total_length_ms / chunk_length_ms)

    chunk_paths = []

    for i in range(total_chunks):
        start = i * chunk_length_ms
        end = min(start + chunk_length_ms, total_length_ms)

        chunk = audio[start:end]

        chunk_path = f"{file_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")

        chunk_paths.append(chunk_path)

    return chunk_paths, total_length_ms


# =========================
# LOW LEVEL: ONE CHUNK
# =========================


def transcribe_chunk(chunk_path):
    """
    Распознаёт один уже подготовленный WAV-чанк.
    Не вызывает normalize_audio().
    """

    segments, info = model.transcribe(
        chunk_path,
        beam_size=5,
        best_of=5,
        temperature=0,
        condition_on_previous_text=False,  
        vad_filter=True,
        vad_parameters={
            "min_silence_duration_ms": 2000,
            "speech_pad_ms": 300,
        },
    )

    result = []

    for segment in segments:
        text = segment.text.strip()

        if not text:
            continue

        result.append({"start": segment.start, "end": segment.end, "text": text})

    return result, info


# =========================
# TEXT UTILS
# =========================


def segments_to_text(segments):
    """
    Превращает сегменты в обычный текст.
    Таймкоды пока оставляем — они полезны для диагностики.
    """

    lines = []

    for s in segments:
        line = f"[{round(s['start'], 1)}s] {s['text']}"
        lines.append(line)

    return "\n".join(lines)


def clean_transcript(text):
    """
    Базовая чистка транскрипции.

    Сейчас делаем аккуратно:
    - убираем пустые строки
    - режем повторы одинаковых строк 3+ подряд
    - режем слишком короткий мусор
    """

    if not text:
        return ""

    lines = text.splitlines()
    cleaned_lines = []

    previous_line = None
    repeat_count = 0

    for line in lines:
        line = line.strip()

        if not line:
            continue
        
        compare_line = re.sub(r"^\[\d+(\.\d+)?s\]\s*", "", line).strip()

        if compare_line == previous_line:
            repeat_count += 1
        else:
            repeat_count = 1
            previous_line = compare_line

        if repeat_count > 3:
            continue

        # Убираем строки, где почти нет букв/цифр
        useful_chars = re.findall(r"[A-Za-zА-Яа-яЁё0-9]", line)
        if len(useful_chars) < 3:
            continue

        # Защита от одинаковых повторов подряд
        # Например:
        # Сиан, Домклик
        # Сиан, Домклик
        # Сиан, Домклик
        if line == previous_line:
            repeat_count += 1
        else:
            repeat_count = 1
            previous_line = line

        if repeat_count >= 3:
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# =========================
# DEBUG / CONTROL LOGS
# =========================
# Этот блок специально оставляем как контрольную точку.
# Если потом надо будет чистить production-код — ищи по метке:
# [STT CONTROL]


def log_stt_control(message):
    """
    Контрольные логи STT pipeline.
    Можно оставить в production: они помогают ловить обрезания текста.
    """

    print(f"[STT CONTROL] {message}")


# =========================
# HIGH LEVEL: MAIN FUNCTION
# =========================


def transcribe_audio(file_path, chunk_minutes=10):
    """
    Главная функция для внешнего кода.

    ВАЖНО:
    Возвращает ГОТОВУЮ СТРОКУ, а не список сегментов.

    Pipeline:
    audio -> normalize -> split -> STT chunks -> segments -> text -> clean -> return text
    """

    started_at = time.time()

    normalized_path = None
    chunk_paths = []

    try:
        log_stt_control(f"input_file={file_path}")

        # 1. Нормализация один раз
        normalized_path = normalize_audio(file_path)
        log_stt_control(f"normalized_file={normalized_path}")

        # 2. Деление на чанки
        chunk_paths, total_length_ms = split_audio(normalized_path, chunk_minutes)

        total_duration_sec = round(total_length_ms / 1000, 2)

        log_stt_control(
            f"audio_duration_sec={total_duration_sec}, "
            f"chunk_minutes={chunk_minutes}, "
            f"chunks_created={len(chunk_paths)}"
        )

        all_segments = []

        # 3. STT по каждому чанку
        for i, chunk_path in enumerate(chunk_paths):
            chunk_started_at = time.time()

            log_stt_control(f"chunk_{i + 1}/{len(chunk_paths)} start: {chunk_path}")

            try:
                segments, info = transcribe_chunk(chunk_path)

                shift_seconds = i * chunk_minutes * 60

                for seg in segments:
                    all_segments.append(
                        {
                            "start": seg["start"] + shift_seconds,
                            "end": seg["end"] + shift_seconds,
                            "text": seg["text"],
                        }
                    )

                chunk_time = round(time.time() - chunk_started_at, 2)

                chunk_text_len = sum(len(seg["text"]) for seg in segments)

                log_stt_control(
                    f"chunk_{i + 1}/{len(chunk_paths)} done: "
                    f"segments={len(segments)}, "
                    f"text_chars={chunk_text_len}, "
                    f"language={info.language}, "
                    f"time_sec={chunk_time}"
                )

            except Exception as e:
                log_stt_control(f"chunk_{i + 1}/{len(chunk_paths)} ERROR: {e}")
                raise

        # 4. Сегменты -> текст
        raw_text = segments_to_text(all_segments)
        cleaned_text = clean_transcript(raw_text)

        total_time = round(time.time() - started_at, 2)

        log_stt_control(
            f"final: "
            f"segments_total={len(all_segments)}, "
            f"raw_chars={len(raw_text)}, "
            f"cleaned_chars={len(cleaned_text)}, "
            f"time_sec={total_time}"
        )

        return cleaned_text

    finally:
        # 5. Удаляем временные чанки
        for chunk_path in chunk_paths:
            try:
                if os.path.exists(chunk_path):
                    os.remove(chunk_path)
            except Exception as e:
                log_stt_control(f"cleanup chunk error: {chunk_path} | {e}")

        # 6. Удаляем нормализованный файл
        try:
            if normalized_path and os.path.exists(normalized_path):
                os.remove(normalized_path)
        except Exception as e:
            log_stt_control(f"cleanup normalized error: {normalized_path} | {e}")
