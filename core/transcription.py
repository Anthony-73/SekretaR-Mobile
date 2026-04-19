from faster_whisper import WhisperModel

model = WhisperModel(
    "large-v3",
    device="cuda",
    compute_type="float16"
)

def transcribe_audio(file_path):

    segments, info = model.transcribe(
        file_path,
        beam_size=5,
        best_of=5,
        temperature=0,
        vad_filter=True,
        language="ru"
    )

    text = ""

    for segment in segments:
        text += segment.text + " "

    return text.strip()