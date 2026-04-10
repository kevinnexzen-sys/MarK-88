from sqlalchemy.orm import Session
from .models import Automation

def suggest_automation(db: Session, name: str, description: str, pattern_id: int | None = None):
    automation = Automation(name=name, description=description, source_pattern_id=pattern_id, status="suggested")
    db.add(automation)
    db.commit()
    db.refresh(automation)
    return automation
