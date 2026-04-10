from __future__ import annotations
from typing import List, Dict

def sample_workflow_events() -> List[Dict]:
    return [
        {'source': 'desktop', 'event_type': 'active_window', 'payload': 'Chrome - WhatsApp Web', 'confidence': 60},
        {'source': 'desktop', 'event_type': 'tab_switch', 'payload': 'Switched to Sheet Tracker', 'confidence': 58},
    ]
