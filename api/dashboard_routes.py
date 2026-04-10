from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import require_role
from ..monitoring import dashboard_summary
from ..agents.ceo_agent import CEOAgent
from ..financial_tracker import portfolio_stats
from ..settings_service import get_group_settings
import json
from ..models import Agent, Approval, Notification, Task, Command, Worker, Device, Skill, Automation, KnowledgeItem, ProjectInstruction, Preview

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])
ceo = CEOAgent()

@router.get("/summary")
def summary(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    return dashboard_summary(db, ceo.heartbeat())

@router.get("/agents")
def agents(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Agent).all()
    return [{"name": r.name, "role": r.role, "status": r.status, "autonomy_level": r.autonomy_level, "capabilities_json": r.capabilities_json} for r in rows]

@router.get("/approvals")
def approvals(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Approval).order_by(Approval.created_at.desc()).all()
    return [{"id": r.id, "task_id": r.task_id, "status": r.status, "summary": r.summary, "response_note": r.response_note} for r in rows]

@router.get("/notifications")
def notifications(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Notification).order_by(Notification.created_at.desc()).all()
    return [{"id": r.id, "title": r.title, "content": r.content, "level": r.level, "read": r.read} for r in rows]

@router.get("/financials")
def financials(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    return portfolio_stats(db)

@router.get("/drafts")
def drafts(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Task).order_by(Task.created_at.desc()).all()
    out = []
    for r in rows:
        try:
            evaluation = json.loads(r.evaluation_json or '{}')
        except Exception:
            evaluation = {}
        out.append({
            "id": r.id, "title": r.title, "status": r.status, "location": r.location,
            "draft_output": r.draft_output, "final_output": r.final_output,
            "evaluation": evaluation, "estimated_time_saved_minutes": r.estimated_time_saved_minutes,
            "estimated_value_usd": r.estimated_value_usd, "execution_blocked": r.execution_blocked,
            "runtime_note": r.runtime_note
        })
    return out

@router.get('/commands')
def commands(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Command).order_by(Command.created_at.desc()).limit(100).all()
    return [{"id": r.id, "task_id": r.task_id, "target_kind": r.target_kind, "command_type": r.command_type, "status": r.status, "result": r.result} for r in rows]

@router.get('/runtime')
def runtime(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    workers = db.query(Worker).all()
    devices = db.query(Device).all()
    return {
        "workers": [{"worker_id": w.worker_id, "status": w.status, "last_seen": w.last_seen.isoformat() if w.last_seen else None, "capabilities_json": w.capabilities_json} for w in workers],
        "devices": [{"device_id": d.device_id, "status": d.status, "last_seen": d.last_seen.isoformat() if d.last_seen else None, "mac": d.mac} for d in devices],
    }

@router.get('/skills')
def skills(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Skill).order_by(Skill.created_at.desc()).all()
    return [{"id": r.id, "name": r.name, "version": r.version, "status": r.status, "source": r.source, "logic": r.logic} for r in rows]

@router.get('/automations')
def automations(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Automation).order_by(Automation.created_at.desc()).all()
    return [{"id": r.id, "name": r.name, "status": r.status, "description": r.description} for r in rows]

@router.get('/knowledge')
def knowledge(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(KnowledgeItem).order_by(KnowledgeItem.created_at.desc()).all()
    return [{"id": r.id, "project_key": r.project_key, "title": r.title, "body": r.body} for r in rows]

@router.get('/instructions')
def instructions(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(ProjectInstruction).order_by(ProjectInstruction.created_at.desc()).all()
    return [{"id": r.id, "project_key": r.project_key, "instruction": r.instruction} for r in rows]

@router.get('/previews')
def previews(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Preview).order_by(Preview.created_at.desc()).limit(50).all()
    return [{"id": r.id, "task_id": r.task_id, "preview_type": r.preview_type, "left_content": r.left_content, "right_content": r.right_content} for r in rows]


@router.get('/providers')
def providers(db: Session = Depends(get_db)):
    from ..settings_service import get_group
    from ..provider_router import ProviderRouter
    cfg = get_group_settings(db, 'providers')
    decision = ProviderRouter().decide('dashboard providers', mode=cfg.get('mode', 'balanced'))
    return {'configured_mode': cfg.get('mode', 'balanced'), 'decision_preview': decision.__dict__}

@router.get('/voice-policy')
def voice_policy():
    from ..voice_policy import get_voice_policy
    return get_voice_policy()


@router.get("/tasks")
def tasks(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Task).order_by(Task.created_at.desc()).all()
    return [{"id": r.id, "title": r.title, "status": r.status, "location": r.location, "runtime_note": r.runtime_note} for r in rows]

@router.get("/commands")
def commands(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Command).order_by(Command.created_at.desc()).all()
    return [{"id": r.id, "task_id": r.task_id, "status": r.status, "target_kind": r.target_kind, "command_type": r.command_type, "result": r.result} for r in rows]
