from __future__ import annotations
import re
from dataclasses import dataclass

@dataclass
class InterpretedCommand:
    title: str
    location: str = 'cloud'
    action_type: str = ''
    requires_online: bool = False
    requires_worker: bool = False
    draft_hint: str = ''


def interpret_command(text: str) -> InterpretedCommand:
    raw = (text or '').strip()
    lowered = raw.lower()
    if any(k in lowered for k in ['wake pc', 'turn on pc', 'wake computer']):
        return InterpretedCommand(title='Wake office PC', location='pc_agent', action_type='wake_pc', requires_online=True)
    if any(k in lowered for k in ['restart pc', 'reboot computer']):
        return InterpretedCommand(title='Restart office PC', location='pc_agent', action_type='restart_pc', requires_online=True)
    if 'whatsapp' in lowered and any(k in lowered for k in ['send', 'reply', 'message']):
        return InterpretedCommand(title=f'WhatsApp action: {raw}', location='desktop_worker', action_type='whatsapp_send', requires_online=True, requires_worker=True)
    if 'browser' in lowered or 'open page' in lowered:
        return InterpretedCommand(title=f'Browser action: {raw}', location='desktop_worker', action_type='browser_open', requires_online=True, requires_worker=True)
    if 'sheet' in lowered or 'excel' in lowered:
        return InterpretedCommand(title=f'Sheet update draft: {raw}', location='cloud', action_type='sheet_upsert', requires_online=True)
    if 'email' in lowered or 'gmail' in lowered:
        return InterpretedCommand(title=f'Email action draft: {raw}', location='cloud', action_type='email_send', requires_online=True)
    if 'calendar' in lowered or 'reminder' in lowered:
        return InterpretedCommand(title=f'Calendar action draft: {raw}', location='cloud', action_type='calendar_create', requires_online=True)
    if any(k in lowered for k in ['work order', 'fill excel', 'fill sheet', 'find work order']):
        return InterpretedCommand(title=f'Work order automation draft: {raw}', location='cloud', action_type='workorder_sheet_draft', requires_online=True)
    if any(k in lowered for k in ['estimate', 'invoice', 'inspection report']):
        return InterpretedCommand(title=f'Draft business document: {raw}', location='cloud', action_type='draft_text', requires_online=False)
    if any(k in lowered for k in ['code', 'app', 'generate app']):
        return InterpretedCommand(title=f'Codegen draft: {raw}', location='cloud', action_type='codegen', requires_online=False)
    return InterpretedCommand(title=f'General draft task: {raw}', location='cloud', action_type='draft_text', requires_online=False)
