import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_upcoming_events(max_events=5):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next `max_events` events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=now,
            maxResults=max_events, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            return "You have no upcoming events."

        # Format the output string
        response_string = "Here are your upcoming events: "
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            # Parse and format the time
            dt_obj = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
            event_time = dt_obj.astimezone().strftime('%I:%M %p') # Local time
            response_string += f"{event['summary']} at {event_time}. "
        return response_string

    except Exception as e:
        return f"An error occurred with the Calendar API: {e}"