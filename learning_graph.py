from sqlalchemy.orm import Session
from .models import LearningEvent, Pattern, Skill, Automation


def merged_learning_graph(db: Session):
    events = db.query(LearningEvent).all()
    by_source = {}
    by_type = {}
    for e in events:
        by_source[e.source] = by_source.get(e.source, 0) + 1
        key = f"{e.source}:{e.event_type}"
        by_type[key] = by_type.get(key, 0) + 1
    patterns = db.query(Pattern).order_by(Pattern.frequency.desc()).all()
    skills = db.query(Skill).order_by(Skill.created_at.desc()).all()
    autos = db.query(Automation).order_by(Automation.created_at.desc()).all()
    return {
        "event_count": len(events),
        "source_counts": by_source,
        "type_counts": by_type,
        "pattern_count": len(patterns),
        "skill_count": len(skills),
        "automation_count": len(autos),
        "top_patterns": [{"title": p.title, "frequency": p.frequency, "confidence": p.confidence} for p in patterns[:10]],
        "recent_skills": [{"name": s.name, "source": s.source, "status": s.status} for s in skills[:10]],
        "recent_automations": [{"name": a.name, "status": a.status} for a in autos[:10]],
    }
