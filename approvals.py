from sqlalchemy.orm import Session
from .models import Approval, Task, Notification

def create_approval(db: Session, task_id: int, summary: str, requested_for: str = "approver"):
    approval = Approval(task_id=task_id, summary=summary, requested_for=requested_for, status="pending")
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return approval

def set_approval_status(db: Session, approval_id: int, status: str, note: str = ""):
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        return None
    approval.status = status
    approval.response_note = note
    task = db.query(Task).filter(Task.id == approval.task_id).first()
    if task:
        if status == 'approved':
            task.status = 'approved'
            task.execution_blocked = False
        elif status == 'rejected':
            task.status = 'rejected'
            task.execution_blocked = True
        db.add(Notification(title=f"Approval {status}", content=f"Task {task.title} is now {task.status}", level='info'))
    db.commit()
    db.refresh(approval)
    return approval

def list_pending_approvals(db: Session):
    return db.query(Approval).filter(Approval.status == "pending").all()


def create_approval_for_task(db: Session, task_id: int, summary: str = ""):
    existing = db.query(Approval).filter(Approval.task_id == task_id, Approval.status.in_(["pending","approved"])).order_by(Approval.created_at.desc()).first()
    if existing and existing.status == "pending":
        return existing
    row = Approval(task_id=task_id, status="pending", summary=summary or f"Approval required for task {task_id}")
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
