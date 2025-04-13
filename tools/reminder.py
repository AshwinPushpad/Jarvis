from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import os

# If modifying these scopes, delete token.json
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def create_google_calendar_reminder(title: str, description: str, start_time: str, duration_minutes: int = 30):
    """
    Creates a reminder in Google Calendar.

    Args:
        title (str): Title of the reminder.
        description (str): Description or notes.
        start_time (str): ISO 8601 formatted time (e.g., '2025-04-11T10:00:00').
        duration_minutes (int): Duration in minutes.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    start_dt = datetime.datetime.fromisoformat(start_time)
    end_dt = start_dt + datetime.timedelta(minutes=duration_minutes)

    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('✅ Event created: %s' % (event.get('htmlLink')))

create_google_calendar_reminder(title="Test", description="Test", start_time="2025-04-11T10:00:00")