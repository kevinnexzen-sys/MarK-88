from __future__ import annotations
import re
from urllib.parse import quote


def parse_whatsapp_message(text: str) -> dict:
    lowered = (text or '').lower().strip()
    if any(k in lowered for k in ['wake pc', 'restart pc', 'shutdown pc']):
        return {'intent': 'device_control', 'raw': text}
    if any(k in lowered for k in ['estimate', 'invoice', 'work order', 'sheet']):
        return {'intent': 'task_request', 'raw': text, 'forwarded': extract_forwarded_block(text)}
    if any(k in lowered for k in ['approve', 'reject']):
        return {'intent': 'approval', 'raw': text}
    return {'intent': 'chat', 'raw': text}


def extract_forwarded_block(text: str) -> dict:
    lines = [l.strip() for l in (text or '').splitlines() if l.strip()]
    work_order = next((l.split(':',1)[1].strip() for l in lines if l.lower().startswith('work order:')), '')
    address = next((l.split(':',1)[1].strip() for l in lines if l.lower().startswith('address:')), '')
    issue = next((l.split(':',1)[1].strip() for l in lines if l.lower().startswith('issue:')), '')
    sender = next((l.split(':',1)[1].strip() for l in lines if l.lower().startswith('sender:')), '')
    return {'work_order': work_order, 'address': address, 'issue': issue, 'sender': sender}


def build_whatsapp_url(phone_or_group: str, message: str) -> str:
    target = phone_or_group.strip()
    return f"https://web.whatsapp.com/send?phone={target}&text={quote(message)}"
