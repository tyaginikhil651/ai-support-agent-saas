from calendar_service import get_calendar_service
from calendar_service import create_event

link = create_event(
    "My internet is not working",
    "2026-06-23T15:00:00",
    "2026-06-23T16:00:00"
)

print(link)

service = get_calendar_service()

print("Connected")