# --- стандартная библиотека ---
import os
import logging
from datetime import datetime, time, timezone, timedelta

# --- сторонние библиотеки ---
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Form

# --- локальные модули проекта ---
from backend.app.db import get_db
from backend.app.db import engine, Base

from backend.users import models
from backend.users.service import get_or_create_user
from backend.users.models import Meeting


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/history/{user_id}")
def get_history(user_id: str, db: Session = Depends(get_db)):
    meetings = (
        db.query(Meeting)
        .filter(Meeting.user_id == user_id)
        .order_by(Meeting.created_at.desc())
        .all()
    )

    return [
        {"id": m.id, "summary": m.summary, "created_at": m.created_at} for m in meetings
    ]


@app.get("/meeting/{meeting_id}")
def get_meeting(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting:
        return {"error": "not found"}

    return {
        "id": meeting.id,
        "summary": meeting.summary,
        "transcript": meeting.transcript,
    }


def create_calendar_event_for_task(task, calendar_service, events_results):
    """
    Создаёт событие в Google Calendar для задачи на основе task.due_date.
    Поведение соответствует циклу в confirm_tasks (те же статусы, поля и разбор дат).
    """
    import re

    task_text = task.get("text") or ""
    due_raw = task.get("due_date")

    if due_raw is None or (isinstance(due_raw, str) and not due_raw.strip()):
        events_results.append({
            "task": task_text,
            "status": "skipped_no_due_date",
            "calendar_link": None,
        })
        return

    # Привести к строке как в запросе confirm_tasks (datetime → ISO)
    if isinstance(due_raw, datetime):
        dt = due_raw
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        due_str = dt.isoformat().replace("+00:00", "Z")
    elif isinstance(due_raw, str):
        due_str = due_raw.strip()
    else:
        events_results.append({
            "task": task_text,
            "status": "skipped_invalid_due_date",
            "calendar_link": None,
        })
        return

    try:
        # Create event for this task — как в confirm_tasks
        assignee = task.get("assignee")

        display_assignee = assignee if assignee else "Без ответственного"

        base_text = (task_text[:97] + "...") if len(task_text) > 100 else task_text

        summary = f"{display_assignee}: {base_text}"

        description = f"Задача из встречи: {task_text}"

       
        
        if assignee:
            description += f"\nОтветственный: {assignee}"

        if re.fullmatch(r"\d{4}-\d{2}-\d{2}$", due_str):
            due_datetime = datetime.fromisoformat(due_str)
            end_datetime = due_datetime.replace(hour=10)
            due_iso = due_datetime.isoformat() + "Z"
            end_iso = end_datetime.isoformat() + "Z"
        else:
            try:
                due_datetime = datetime.fromisoformat(due_str.replace("Z", "+00:00"))
                end_datetime = due_datetime.replace(
                    hour=due_datetime.hour + 1 if due_datetime.hour < 23 else 23
                )
                due_iso = due_datetime.isoformat().replace("+00:00", "Z")
                end_iso = end_datetime.isoformat().replace("+00:00", "Z")
            except Exception:
                events_results.append({
                    "task": task_text,
                    "status": "skipped_invalid_due_date",
                    "calendar_link": None,
                })
                return

        event = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": due_iso,
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_iso,
                "timeZone": "UTC",
            },
        }
        created_event = calendar_service.events().insert(
            calendarId="primary",
            body=event,
        ).execute()

        events_results.append({
            "task": task_text,
            "status": "created",
            "calendar_link": created_event.get("htmlLink"),
            "event_id": created_event.get("id"),
        })
    except Exception as e:
        events_results.append({
            "task": task_text,
            "status": f"error: {str(e)}",
            "calendar_link": None,
        })

from core.transcription import transcribe_audio
from core.llm_analysis import make_summary, extract_tasks
from core.calendar_integration import create_event


# ================= PATH =================
BASE_DIR = "data/meetings"
os.makedirs(BASE_DIR, exist_ok=True)


# ================= ROOT API =================
@app.get("/api")
def root():
    return {"status": "SekretaR Mobile backend работает"}


# ================= UPLOAD =================
@app.post("/upload")
async def upload_audio(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    db: Session = Depends(get_db),
):

    # создаём папку встречи
    meeting_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    meeting_path = os.path.join(BASE_DIR, meeting_id)
    os.makedirs(meeting_path, exist_ok=True)

    # сохраняем аудио
    audio_path = os.path.join(meeting_path, file.filename)
    with open(audio_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # ================= TRANSCRIPTION =================
    try:
        text = transcribe_audio(audio_path)
    except Exception as e:
        return {"error": f"transcription error: {str(e)}"}

    # сохраняем текст
    transcript_path = os.path.join(meeting_path, "transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(text)

    # ================= SUMMARY =================
    try:
        summary = make_summary(text)
    except Exception as e:
        summary = f"Ошибка генерации summary: {str(e)}"

    summary_path = os.path.join(meeting_path, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    # ================= TASKS =================
    try:
        raw_tasks = extract_tasks(text)
        # Structure each task as a dict (text, due_date, assignee)
        tasks = [
            {"text": t, "due_date": None, "assignee": None}
            for t in raw_tasks
        ]
    except Exception as e:
        tasks = [{
            "text": f"Ошибка извлечения задач: {str(e)}", 
            "due_date": None, 
            "assignee": None
        }]

    # Save tasks to file (as bullet points just for compatibility/logging)
    tasks_path = os.path.join(meeting_path, "tasks.txt")
    with open(tasks_path, "w", encoding="utf-8") as f:
        for task in tasks:
            f.write(f"- {task['text']}\n")

    # --- SAVE TO DB ---
    try:
        db.add(
            Meeting(id=meeting_id, user_id=user_id, summary=summary, transcript=text)
        )
        db.commit()
    except Exception as e:
        print("DB SAVE ERROR:", e)

    # ================= RESPONSE =================
    return {
        "status": "ok",
        "next_actions": ["add_to_calendar", "export_doc"],
        "meeting_id": meeting_id,
        "transcript": text,
        "summary": summary,
        "tasks": tasks,  # structured tasks!
        # No calendar link yet, will be produced after confirm_tasks
        "calendar_link": None,
    }


# ================= CONFIRM TASKS ENDPOINT =================
from fastapi import Body

from typing import List, Optional
from pydantic import BaseModel

class TaskCreate(BaseModel):
    text: str
    due_date: Optional[str] = None
    assignee: Optional[str] = None

class ConfirmTasksRequest(BaseModel):
    meeting_id: str
    summary: str
    tasks: List[TaskCreate]

@app.post("/confirm_tasks")
async def confirm_tasks(data: ConfirmTasksRequest):
    """
    Accepts:
        - meeting_id: str
        - summary: str
        - tasks: list of {text, due_date, assignee}
    Creates a calendar event for each task with due_date and assignee.
    Returns the list of created event links (with metadata).
    """
    from core.calendar_integration import get_calendar_service

    events_results = []
    service = get_calendar_service()

    meeting_path = os.path.join(BASE_DIR, data.meeting_id)
    os.makedirs(meeting_path, exist_ok=True)
    confirmed_path = os.path.join(meeting_path, "confirmed_tasks.txt")
    with open(confirmed_path, "w", encoding="utf-8") as f:
        for task in data.tasks:
            # Write to file with all fields
            assignee_part = f", assignee: {task.assignee}" if task.assignee else ""
            due_part = f", due: {task.due_date}" if task.due_date else ""
            f.write(f"- {task.text}{due_part}{assignee_part}\n")

    for task in data.tasks:
        if not task.due_date:
            events_results.append({
                "task": task.text,
                "status": "skipped_no_due_date",
                "calendar_link": None
            })
            continue

        create_calendar_event_for_task(
            {"text": task.text, "due_date": task.due_date, "assignee": task.assignee},
            service,
            events_results,
        )

    print(events_results)
    created_links = [
        ev["calendar_link"] for ev in events_results if ev["calendar_link"]
    ]

    return {
        "status": "ok" if created_links else "error",
        "calendar_link": created_links[0] if created_links else None,
    }


@app.get("/db_check")
def db_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT version();")).fetchone()
    return {"db_version": result[0]}


# ================= STATIC (WEB UI) =================
app.mount("/", StaticFiles(directory="backend/app/static", html=True), name="static")
