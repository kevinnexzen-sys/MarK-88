from __future__ import annotations
from sqlalchemy.orm import Session
from .models import Task
from .runtime_executor import execute_task_if_approved


def autonomy_tick(db: Session) -> dict:
    waiting = db.query(Task).filter(Task.status == "waiting_approval").count()
    approved = 0
    executed = 0
    for task in db.query(Task).filter(Task.status == "approved").order_by(Task.priority.asc(), Task.created_at.asc()).all():
        if task.execution_blocked:
            continue
        # parent tasks wait for approved/completed children first
        children = db.query(Task).filter(Task.parent_task_id == task.id).all()
        if children and any(c.status not in {"completed", "approved"} for c in children):
            continue
        approved += 1
        result = execute_task_if_approved(db, task)
        if result.get("status") in {"completed", "queued"}:
            executed += 1
    return {
        "waiting_approval": waiting,
        "approved_ready": approved,
        "executed_this_tick": executed,
    }
