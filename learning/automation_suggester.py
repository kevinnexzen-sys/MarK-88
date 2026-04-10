from __future__ import annotations
from sqlalchemy.orm import Session
from ..models import Pattern
from ..automation_engine import suggest_automation
from ..skills_engine import create_skill


def propose_automations(db: Session):
    suggestions = []
    for pattern in db.query(Pattern).filter(Pattern.frequency >= 2).all():
        auto = suggest_automation(db, name=f"Automate {pattern.title}", description=f"Automation based on {pattern.fingerprint}", pattern_id=pattern.id)
        suggestions.append(auto)
        if pattern.frequency >= 4:
            create_skill(db, name=f"Skill for {pattern.title[:50]}", logic=f"Auto-generated from pattern {pattern.fingerprint}", source="pattern_detection")
    return suggestions
