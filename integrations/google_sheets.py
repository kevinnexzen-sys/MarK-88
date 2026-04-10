import json
from typing import Any

from ..settings_service import get_setting


def _client_from_settings(db):
    raw = get_setting(db, 'google', 'service_account_json', '')
    if not raw:
        raise RuntimeError('Missing google.service_account_json setting')
    info = json.loads(raw)
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    return build('sheets', 'v4', credentials=creds, cache_discovery=False)


def upsert_row(db, sheet_id: str, tab: str, key_column: str, row: dict[str, Any]):
    service = _client_from_settings(db)
    sheet = service.spreadsheets()
    values = sheet.values().get(spreadsheetId=sheet_id, range=f"{tab}!A:ZZ").execute().get('values', [])
    if not values:
        headers = list(row.keys())
        body = {'values': [headers, [str(row.get(h, '')) for h in headers]]}
        sheet.values().update(spreadsheetId=sheet_id, range=f"{tab}!A1", valueInputOption='USER_ENTERED', body=body).execute()
        return {'status': 'inserted', 'row_index': 2, 'headers': headers}

    headers = values[0]
    if key_column not in headers:
        headers.append(key_column)
    for k in row.keys():
        if k not in headers:
            headers.append(k)
    key_idx = headers.index(key_column)
    target_index = None
    key_value = str(row.get(key_column, ''))
    for idx, existing in enumerate(values[1:], start=2):
        if key_idx < len(existing) and str(existing[key_idx]) == key_value:
            target_index = idx
            break
    data = [str(row.get(h, '')) for h in headers]
    header_range = f"{tab}!A1:{chr(64+min(len(headers),26))}1" if len(headers)<=26 else f"{tab}!A1"
    sheet.values().update(spreadsheetId=sheet_id, range=header_range, valueInputOption='USER_ENTERED', body={'values': [headers]}).execute()
    if target_index is None:
        target_index = len(values) + 1
        status = 'inserted'
    else:
        status = 'updated'
    row_range = f"{tab}!A{target_index}"
    sheet.values().update(spreadsheetId=sheet_id, range=row_range, valueInputOption='USER_ENTERED', body={'values': [data]}).execute()
    return {'status': status, 'row_index': target_index, 'headers': headers}
