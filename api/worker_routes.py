import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Worker, Command
from ..schemas import WorkerRegisterRequest
from ..auth import require_role
from ..runtime_executor import complete_command

router = APIRouter(prefix="/api/workers", tags=["workers"])

@router.post("/register")
def register(payload: WorkerRegisterRequest, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.worker_id == payload.worker_id).first()
    if not worker:
        worker = Worker(worker_id=payload.worker_id, name=payload.name, worker_type=payload.worker_type)
        db.add(worker)
    worker.status = "online"
    worker.last_seen = datetime.utcnow()
    worker.capabilities_json = json.dumps(payload.capabilities)
    db.commit(); db.refresh(worker)
    return {"status": "ok", "worker_id": worker.worker_id}

@router.post("/heartbeat")
def heartbeat(payload: dict, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.worker_id == payload.get('worker_id')).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    worker.status = "online"
    worker.last_seen = datetime.utcnow()
    if payload.get('capabilities') is not None:
        worker.capabilities_json = json.dumps(payload.get('capabilities'))
    db.commit()
    return {"status": "ok", "last_seen": worker.last_seen.isoformat()}

@router.get("")
def list_workers(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Worker).all()
    return [{"id": r.id, "worker_id": r.worker_id, "name": r.name, "status": r.status, "worker_type": r.worker_type, "last_seen": r.last_seen.isoformat() if r.last_seen else None, "capabilities_json": r.capabilities_json} for r in rows]

@router.get("/{worker_id}")
def get_worker(worker_id: str, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    r = db.query(Worker).filter(Worker.worker_id == worker_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Worker not found")
    return {"id": r.id, "worker_id": r.worker_id, "name": r.name, "status": r.status, "capabilities_json": r.capabilities_json}

@router.get("/{worker_id}/commands")
def poll_commands(worker_id: str, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.worker_id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    cmds = db.query(Command).filter(Command.worker_id == worker.id, Command.status == 'pending').order_by(Command.created_at.asc()).all()
    out = []
    for c in cmds:
        try:
            payload = json.loads(c.payload_json or '{}')
        except Exception:
            payload = {}
        out.append({"id": c.id, "command_type": c.command_type, "command_text": c.command_text, "payload": payload, "task_id": c.task_id})
    return out

@router.post("/{worker_id}/commands/{command_id}/complete")
def complete_worker_command(worker_id: str, command_id: int, payload: dict, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.worker_id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    cmd = db.query(Command).filter(Command.id == command_id, Command.worker_id == worker.id).first()
    if not cmd:
        raise HTTPException(status_code=404, detail="Command not found")
    complete_command(db, cmd, payload.get('result', ''), payload.get('status', 'completed'))
    return {"status": "ok"}
