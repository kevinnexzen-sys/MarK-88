from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import require_role
from ..schemas import TaskCreateRequest
from ..command_parser import interpret_command
from ..task_queue import create_task

router = APIRouter(prefix="/api/commands", tags=["commands"])

@router.post("/interpret")
def interpret(payload: dict, db: Session = Depends(get_db), _=Depends(require_role(["admin","manager","approver","operator"]))):
    text = payload.get("text","")
    parsed = interpret_command(text)
    task = create_task(db, TaskCreateRequest(
        title=parsed["title"],
        description=parsed["description"],
        source=payload.get("source","mobile_voice"),
        priority=int(payload.get("priority",5)),
        project_key=payload.get("project_key","default"),
        provider_mode=payload.get("provider_mode","balanced"),
        requires_online=parsed["requires_online"],
        requires_worker=parsed["requires_worker"],
        action_type=parsed.get("action_type",""),
        action_payload=parsed.get("action_payload",{}),
    ))
    return {"parsed": parsed, "task_id": task.id, "status": task.status}
