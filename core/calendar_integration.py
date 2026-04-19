from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service


def create_event(summary: str, tasks: list):
    service = get_calendar_service()

    now = datetime.datetime.utcnow()
    end = now + datetime.timedelta(hours=1)

    description = "\n".join(tasks)

    event = {
        "summary": summary[:100],
        "description": description,
        "start": {
            "dateTime": now.isoformat() + "Z",
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": end.isoformat() + "Z",
            "timeZone": "UTC",
        },
    }

    event = service.events().insert(calendarId="primary", body=event).execute()

    return event.get("htmlLink")
