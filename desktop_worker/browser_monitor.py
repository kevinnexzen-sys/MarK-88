from __future__ import annotations
from typing import List, Dict

def normalize_browser_events(events: List[Dict]) -> List[Dict]:
    out = []
    for e in events:
        out.append({
            'source': 'desktop',
            'event_type': e.get('event_type', 'browser_event'),
            'payload': f"{e.get('title','')} | {e.get('url','')}",
            'confidence': int(e.get('confidence', 55)),
        })
    return out
