from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import require_role
from ..memory_engine import remember, search_memory
from ..models import MemoryEntry, Skill, Automation, KnowledgeItem, ProjectInstruction

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

@router.get("/memory")
def memory(q: str = "", db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = search_memory(db, q) if q else db.query(MemoryEntry).order_by(MemoryEntry.created_at.desc()).all()
    return [{"id": r.id, "title": r.title, "type": r.entry_type, "project_key": r.project_key, "content": r.content} for r in rows]

@router.post("/memory")
def add_memory(title: str, content: str, entry_type: str = "general", project_key: str = "default", db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "operator"]))):
    item = remember(db, title=title, content=content, entry_type=entry_type, project_key=project_key)
    return {"id": item.id}

@router.get("/skills")
def skills(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Skill).all()
    return [{"id": r.id, "name": r.name, "version": r.version, "status": r.status, "source": r.source} for r in rows]

@router.get("/automations")
def automations(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Automation).all()
    return [{"id": r.id, "name": r.name, "status": r.status, "description": r.description} for r in rows]

@router.get("/knowledge-base")
def knowledge_base(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(KnowledgeItem).all()
    return [{"id": r.id, "project_key": r.project_key, "title": r.title, "body": r.body} for r in rows]

@router.get("/instructions")
def instructions(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(ProjectInstruction).all()
    return [{"id": r.id, "project_key": r.project_key, "instruction": r.instruction} for r in rows]
