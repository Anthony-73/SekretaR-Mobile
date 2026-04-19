import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def ask_llm(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    return data.get("response", "").strip()


# ================= SUMMARY =================
def make_summary(text: str) -> str:
    prompt = f"""
Ты — бизнес-аналитик совещаний.

Отвечай строго на русском языке.

Сформируй результат в СТРУКТУРЕ:

1. РЕШЕНИЕ ВСТРЕЧИ (1-2 предложения)
2. КЛЮЧЕВЫЕ ВЫВОДЫ (список)
3. ЭКОНОМИКА (если есть цифры)
4. РИСКИ / ПРОБЛЕМЫ (если обсуждались)

ПРАВИЛА:
- не выдумывай факты
- можно обобщать смысл
- убирай повторы
- только суть, без воды

Текст:
{text}
"""
    return ask_llm(prompt)


# ================= TASKS =================
def extract_tasks(text: str):
    prompt = f"""
Ты — руководитель проекта.

Отвечай строго на русском языке.

Выдели задачи из разговора.

ПРАВИЛА:
- каждая строка = одна задача
- начинай с глагола
- только конкретные действия
- без пояснений и лишнего текста

Текст:
{text}
"""

    raw = ask_llm(prompt)

    lines = raw.split("\n")

    tasks = []

    import re

    for line in lines:
        cleaned = line.strip().strip("-•* ").strip()

        # Убираем нумерацию в начале строки, например "1. "
        cleaned = re.sub(r"^\d+\.\s*", "", cleaned)

        if not cleaned:
            continue
     

        if len(cleaned.split()) < 2:
            continue

        forbidden_words = [
            "начать", "выступить", "обсудить", "рассмотреть", "провести совещание",
            "присутствовать", "выступит", "выступал", "доклад"
        ]
        cleaned_lower = cleaned.lower()
   

        if any(cleaned_lower.startswith(word) for word in forbidden_words):
            continue
            
        if any(word in cleaned_lower for word in ["доклад", "присутствовать"]):
            continue      
        tasks.append(cleaned)

    return tasks