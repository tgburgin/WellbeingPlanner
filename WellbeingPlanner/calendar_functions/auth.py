import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Constants
SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = 'token.json'

def initialize_calendar_service():
    creds = None

    # Check if the token file exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials are available, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh the token if expired
        else:
            # Create the flow using environment variables
            client_config = {
                "installed": {
                    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                    "redirect_uris": ["http://localhost"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "project_id": os.getenv("GOOGLE_PROJECT_ID")
                }
            }
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials to the token file
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def get_or_create_calendar(service):
    # Check if the calendar already exists
    calendar_name = "Wellbeing"

    calendars = service.calendarList().list().execute()
    for calendar in calendars.get('items', []):
        if calendar['summary'] == calendar_name:
            print(f"Found existing calendar: {calendar_name} (ID: {calendar['id']})")
            return calendar['id']

    new_calendar = {
        'summary': calendar_name,
        'timeZone': 'Europe/London'
    }
    created_calendar = service.calendars().insert(body=new_calendar).execute()
    print(f"Created new calendar: {calendar_name} (ID: {created_calendar['id']})")
    return created_calendar['id']

def get_calendar_colors(service):
    return service.colors().get().execute().get('calendar', {})
