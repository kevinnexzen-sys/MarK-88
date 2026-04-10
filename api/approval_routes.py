from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import require_role
from ..schemas import ApprovalActionRequest
from ..approvals import set_approval_status
from ..models import Approval, Task
from ..runtime_executor import execute_task_if_approved

router = APIRouter(prefix="/api/approvals", tags=["approvals"])

@router.get("")
def list_all(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Approval).all()
    return [{"id": r.id, "task_id": r.task_id, "status": r.status, "summary": r.summary} for r in rows]

@router.post("/{approval_id}")
def act(approval_id: int, payload: ApprovalActionRequest, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver"]))):
    row = set_approval_status(db, approval_id, payload.status, payload.response_note)
    if not row:
        raise HTTPException(status_code=404, detail="Approval not found")
    result = None
    if payload.status == 'approved':
        task = db.query(Task).filter(Task.id == row.task_id).first()
        if task:
            result = execute_task_if_approved(db, task)
    return {"id": row.id, "status": row.status, "execution": result}

@router.post('/task/{task_id}/approve')
def approve_by_task(task_id: int, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver"]))):
    row = db.query(Approval).filter(Approval.task_id == task_id).order_by(Approval.created_at.desc()).first()
    if not row:
        raise HTTPException(status_code=404, detail='Approval not found')
    row = set_approval_status(db, row.id, 'approved', '')
    task = db.query(Task).filter(Task.id == task_id).first()
    result = execute_task_if_approved(db, task) if task else None
    return {'id': row.id, 'status': row.status, 'execution': result}

@router.post('/task/{task_id}/reject')
def reject_by_task(task_id: int, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver"]))):
    row = db.query(Approval).filter(Approval.task_id == task_id).order_by(Approval.created_at.desc()).first()
    if not row:
        raise HTTPException(status_code=404, detail='Approval not found')
    row = set_approval_status(db, row.id, 'rejected', '')
    return {'id': row.id, 'status': row.status}
