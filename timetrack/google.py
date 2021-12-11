""" handles authentication with Google calendar """
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def authenticate_build_service(creds_path, client_config):
    """If the credentials creds are not valid or None, they are renewed or
    a login procedure is started. Returns the Google api service object and
    valid credentials

    Args:
        creds: `google.oauth2.credentials.Credentials` The OAuth 2.0 credentials for the user. Set to None if non
        existing.
        client_config: (Mapping[str, Any]): The client configuration in the Google
        client secrets`_ format.
    Returns:
        A Resource object with methods for interacting with the calendar service.

    """
    creds = None

    if os.path.exists(creds_path):
        creds = Credentials.from_authorized_user_file(creds_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run

    with open(creds_path, 'w') as token:
        token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)

    return service


class GoogleCalendar:

    def __init__(self, service):
        self._service = service

    def get_calendars(self):
        """
        Get calendars
        Returns: List
        """
        return self._service.calendarList().list().execute()['items']

    def get_events(self, calendar_id, start, end):
        """
        fetch all events from the Google calendar API between start and end.
        Args:
            calendar_id: Calendar id to fetch events from
            start: datetime object
            end: datetime object

        Returns: List of events

        """
        events = []
        next_page_token = None
        while True:
            events_result = self._service.events().list(calendarId=calendar_id,
                                                        timeMin=start.isoformat() + 'Z',
                                                        timeMax=end.isoformat() + 'Z',
                                                        singleEvents=True,
                                                        maxResults=2500,
                                                        pageToken=next_page_token,
                                                        orderBy='startTime')\
                .execute()
            events += events_result.get('items', [])
            next_page_token = events_result.get('nextPageToken', None)
            if next_page_token is None:
                break
        return events
    