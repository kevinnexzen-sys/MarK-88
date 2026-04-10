from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import require_role
from ..learning.watch_to_learn import record_watch_event, record_watch_batch, sequence_patterns
from ..learning.pattern_detector import analyze_patterns
from ..learning.automation_suggester import propose_automations
from ..learning.search_to_skill import convert_search_to_skill
from ..learning.self_improver import self_improve_snapshot
from ..learning_graph import merged_learning_graph
from ..models import Approval, Skill, Automation, Pattern, LearningEvent

router = APIRouter(prefix="/api/learning", tags=["learning"])

@router.post('/events')
def create_event(payload: dict, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "operator"]))):
    row = record_watch_event(db, payload.get('source','desktop'), payload.get('event_type','unknown'), payload.get('payload',''), int(payload.get('confidence',60)), payload.get('project_key','default'))
    return {"id": row.id}

@router.post('/events/batch')
def create_event_batch(payload: dict, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "operator"]))):
    rows = record_watch_batch(db, payload.get('source','desktop'), payload.get('events',[]), payload.get('project_key','default'))
    seq = sequence_patterns(db, payload.get('source'))
    return {"created": len(rows), "sequence_patterns": len(seq)}

@router.post('/analyze')
def analyze(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "operator"]))):
    sequence_patterns(db)
    patterns = analyze_patterns(db)
    automations = propose_automations(db)
    approvals = db.query(Approval).filter(Approval.status=='approved').count()
    rejections = db.query(Approval).filter(Approval.status=='rejected').count()
    successful_skills = db.query(Skill).filter(Skill.status.in_(['ready','active','draft'])).count()
    return {
        "patterns_created": len(patterns),
        "automations_suggested": len(automations),
        "self_improver": self_improve_snapshot(approvals, rejections, successful_skills),
        "graph": merged_learning_graph(db),
    }

@router.post('/search-to-skill')
def search_to_skill(payload: dict, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "operator"]))):
    skill = convert_search_to_skill(db, payload.get('query',''), payload.get('summary',''), payload.get('project_key','default'))
    return {"skill_id": skill.id, "name": skill.name}

@router.get('/graph')
def graph(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    return merged_learning_graph(db)

@router.get('/patterns')
def patterns(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Pattern).order_by(Pattern.frequency.desc()).all()
    return [{"id": r.id, "title": r.title, "frequency": r.frequency, "confidence": r.confidence} for r in rows]

@router.get('/skills')
def skills(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Skill).order_by(Skill.created_at.desc()).all()
    return [{"id": r.id, "name": r.name, "version": r.version, "status": r.status, "source": r.source} for r in rows]

@router.get('/automations')
def automations(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Automation).order_by(Automation.created_at.desc()).all()
    return [{"id": r.id, "name": r.name, "status": r.status, "description": r.description} for r in rows]

@router.get('/events/recent')
def recent_events(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(LearningEvent).order_by(LearningEvent.created_at.desc()).limit(100).all()
    return [{"id": r.id, "source": r.source, "event_type": r.event_type, "payload": r.payload, "confidence": r.confidence} for r in rows]


@router.post('/mobile-event')
def create_mobile_event(payload: dict, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "operator", "viewer", "approver"]))):
    row = record_watch_event(db, 'mobile', payload.get('event_type','screen_view'), payload.get('payload',''), int(payload.get('confidence',70)), payload.get('project_key','default'))
    return {"id": row.id, "source": row.source}

@router.post('/desktop-event')
def create_desktop_event(payload: dict, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "operator"]))):
    row = record_watch_event(db, 'desktop', payload.get('event_type','workflow'), payload.get('payload',''), int(payload.get('confidence',65)), payload.get('project_key','default'))
    return {"id": row.id, "source": row.source}
