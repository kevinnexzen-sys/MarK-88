from collections import Counter
from sqlalchemy.orm import Session
from ..models import LearningEvent, Pattern

def analyze_patterns(db: Session):
    events = db.query(LearningEvent).all()
    counts = Counter((e.source, e.event_type) for e in events)
    created = []
    for (source, event_type), freq in counts.items():
        if freq < 2:
            continue
        fp = f"{source}:{event_type}"
        row = db.query(Pattern).filter(Pattern.fingerprint == fp).first()
        if row:
            row.frequency = freq
        else:
            row = Pattern(title=f"Pattern {source} {event_type}", fingerprint=fp, frequency=freq, confidence=min(95, 40 + freq*5))
            db.add(row)
            created.append(row)
    db.commit()
    return created
