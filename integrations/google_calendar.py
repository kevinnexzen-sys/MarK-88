import json
from datetime import datetime, timedelta, timezone

from ..settings_service import get_setting


def _client_from_settings(db):
    raw = get_setting(db, 'google', 'service_account_json', '')
    if not raw:
        raise RuntimeError('Missing google.service_account_json setting')
    info = json.loads(raw)
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    scopes = ['https://www.googleapis.com/auth/calendar']
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    return build('calendar', 'v3', credentials=creds, cache_discovery=False)


def create_event(db, calendar_id: str, title: str, when: str, description: str = ''):
    service = _client_from_settings(db)
    start_dt = datetime.fromisoformat(when.replace('Z', '+00:00')) if when else datetime.now(timezone.utc)
    end_dt = start_dt + timedelta(hours=1)
    body = {
        'summary': title,
        'description': description,
        'start': {'dateTime': start_dt.isoformat()},
        'end': {'dateTime': end_dt.isoformat()},
    }
    event = service.events().insert(calendarId=calendar_id, body=body).execute()
    return {'status': 'created', 'event_id': event.get('id'), 'htmlLink': event.get('htmlLink')}
