"""
Google Workspace Integration — Calendar and Gmail via OAuth2.
First run triggers a browser-based login, after which credentials are 
cached in data/google_token.json for future sessions.
"""
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
]

TOKEN_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'google_token.json')
CREDS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'google_credentials.json')


def _get_credentials():
    """Returns valid user credentials from storage, triggering OAuth flow if needed."""
    creds = None
    
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDS_PATH):
                return None, "Missing google_credentials.json. Please download it from Google Cloud Console."
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return creds, None


def get_todays_events() -> str:
    """Fetches today's calendar events and returns a readable summary."""
    import datetime
    
    creds, err = _get_credentials()
    if err:
        return err

    service = build('calendar', 'v3', credentials=creds)
    
    now = datetime.datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
    end_of_day = now.replace(hour=23, minute=59, second=59).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_of_day,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    if not events:
        return "You have no events scheduled for today."
    
    lines = ["Here's your schedule for today:"]
    for e in events:
        start = e['start'].get('dateTime', e['start'].get('date', ''))
        if 'T' in start:
            # Parse time from ISO format
            t = start.split('T')[1][:5]
            lines.append(f"  {t} — {e.get('summary', '(No title)')}")
        else:
            lines.append(f"  All day — {e.get('summary', '(No title)')}")
    
    return "\n".join(lines)


def send_gmail(to: str, subject: str, body: str) -> str:
    """Sends an email using the authenticated Gmail account."""
    import base64
    from email.mime.text import MIMEText
    
    creds, err = _get_credentials()
    if err:
        return err

    service = build('gmail', 'v1', credentials=creds)
    
    msg = MIMEText(body)
    msg['to'] = to
    msg['subject'] = subject
    
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    
    service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()
    
    return f"Email sent to {to}."
