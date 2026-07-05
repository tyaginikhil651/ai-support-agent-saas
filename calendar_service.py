from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

def get_calendar_service():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds:

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    return service




def create_event(title, start_time, end_time):

    service = get_calendar_service()

    event = {

        "summary": title,

        "start": {
            "dateTime": start_time,
            "timeZone": "Asia/Kolkata"
        },

        "end": {
            "dateTime": end_time,
            "timeZone": "Asia/Kolkata"
        }
    }

    event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return event["htmlLink"]




def book_appointment(
        user_id,
        service,
        date,
        start_time,
        end_time
):

    event_link = create_event(
        service,
        start_time,
        end_time
    )

    return f"""
Appointment Booked

Service: {service}

Calendar:
{event_link}
"""

