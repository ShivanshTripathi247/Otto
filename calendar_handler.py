import datetime
import os.path
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# This block determines the correct base path for assets
if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_upcoming_events(max_events=3):
    creds = None
    token_path = os.path.join(BASE_PATH, 'token.json')
    creds_path = os.path.join(BASE_PATH, 'credentials.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary', timeMin=now, maxResults=max_events, 
            singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            return "You have no upcoming events."
        response_string = "Here are your upcoming events: "
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            dt_obj = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
            event_time = dt_obj.astimezone().strftime('%I:%M %p')
            response_string += f"{event['summary']} at {event_time}. "
        return response_string
    except Exception as e:
        return f"An error occurred with the Calendar API: {e}"