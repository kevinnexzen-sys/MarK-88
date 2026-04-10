import json
from sqlalchemy.orm import Session

from .integrations.google_sheets import upsert_row
from .integrations.google_calendar import create_event
from .integrations.google_mail import send_mail
from .settings_service import get_setting


def run_task_action(db: Session, task):
    action_type = (task.action_type or '').strip()
    if not action_type:
        return None
    payload = json.loads(task.action_payload_json or '{}')
    if action_type == 'google_sheets_upsert':
        sheet_id = payload.get('sheet_id') or get_setting(db, 'google', 'sheet_id', '')
        tab = payload.get('tab') or get_setting(db, 'google', 'sheet_tab', 'Sheet1')
        key_column = payload.get('key_column') or get_setting(db, 'google', 'sheet_key_column', 'id')
        row = payload.get('row', {})
        return upsert_row(db, sheet_id, tab, key_column, row)
    if action_type == 'email_send':
        return send_mail(db, payload.get('to', ''), payload.get('subject', task.title), payload.get('body', task.description))
    if action_type == 'calendar_create_event':
        calendar_id = payload.get('calendar_id') or get_setting(db, 'google', 'calendar_id', '')
        return create_event(db, calendar_id, payload.get('title', task.title), payload.get('when', ''), payload.get('description', task.description))
    return {'status': 'noop', 'detail': f'Unknown action_type={action_type}'}
