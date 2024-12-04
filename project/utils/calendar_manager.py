from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import os
import pickle

class CalendarManager:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.creds = None
        self.service = None
        self.initialize_credentials()

    def initialize_credentials(self):
        if os.path.exists('calendar_token.pickle'):
            with open('calendar_token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('calendar_token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('calendar', 'v3', credentials=self.creds)

    def create_event(self, summary: str, description: str, start_time: datetime.datetime,
                    end_time: datetime.datetime, attendees: list = None) -> bool:
        try:
            event = {
                'summary': summary,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
            }

            if attendees:
                event['attendees'] = [{'email': email} for email in attendees]

            self.service.events().insert(
                calendarId='primary',
                body=event,
                sendUpdates='all'
            ).execute()
            return True
        except Exception as e:
            print(f"Error creating calendar event: {e}")
            return False

    def get_upcoming_events(self, max_results: int = 10):
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            return events_result.get('items', [])
        except Exception as e:
            print(f"Error fetching upcoming events: {e}")
            return []
