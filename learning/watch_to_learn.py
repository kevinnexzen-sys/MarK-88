from __future__ import annotations
from collections import deque
from hashlib import sha1
from typing import Iterable
from sqlalchemy.orm import Session
from ..models import LearningEvent, Pattern


def record_watch_event(db: Session, source: str, event_type: str, payload: str, confidence: int = 60, project_key: str = "default"):
    event = LearningEvent(source=source, event_type=event_type, payload=payload, confidence=confidence, project_key=project_key)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def record_watch_batch(db: Session, source: str, events: Iterable[dict], project_key: str = "default"):
    created = []
    for item in events:
        created.append(record_watch_event(
            db,
            source=item.get('source', source),
            event_type=item.get('event_type', 'unknown'),
            payload=item.get('payload', ''),
            confidence=int(item.get('confidence', 60)),
            project_key=item.get('project_key', project_key),
        ))
    return created


def sequence_patterns(db: Session, source: str | None = None, max_window: int = 3):
    q = db.query(LearningEvent)
    if source:
        q = q.filter(LearningEvent.source == source)
    events = q.order_by(LearningEvent.created_at.asc()).all()
    if len(events) < 2:
        return []
    created = []
    window = deque(maxlen=max_window)
    for e in events:
        token = f"{e.source}:{e.event_type}:{(e.payload or '')[:40]}"
        window.append(token)
        if len(window) < 2:
            continue
        seq = ' -> '.join(window)
        fp = sha1(seq.encode()).hexdigest()[:24]
        row = db.query(Pattern).filter(Pattern.fingerprint == fp).first()
        if row:
            row.frequency += 1
            row.confidence = min(99, row.confidence + 1)
        else:
            row = Pattern(title=f"Sequence pattern: {window[-1]}", fingerprint=fp, frequency=2, confidence=66)
            db.add(row)
            created.append(row)
    db.commit()
    return created
