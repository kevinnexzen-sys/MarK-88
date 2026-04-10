from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import TaskCreateRequest, TaskUpdateRequest, TaskExecutionRequest
from ..task_queue import create_task, update_task_status
from ..models import Task, TaskStep
from ..auth import require_role
from ..approvals import create_approval
from ..runtime_executor import execute_task_if_approved
from ..agents.planner_agent import PlannerAgent
import json

router = APIRouter(prefix="/api/tasks", tags=["tasks"])
planner = PlannerAgent()

@router.post("")
def create(payload: TaskCreateRequest, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "operator"]))):
    task = create_task(db, payload)
    plan = planner.build_plan(task)
    created_children = []
    for child in plan.get('subtasks', []):
        child_payload = TaskCreateRequest(
            title=child['title'],
            description=f"Child task for parent {task.id}",
            source='planner',
            location=child.get('location', task.location),
            priority=min(task.priority + 1, 10),
            assigned_to='CEO',
            requested_by=task.requested_by,
            project_key=task.project_key,
            provider_mode=task.provider_mode,
            requires_online=child.get('requires_online', task.requires_online),
            requires_worker=child.get('requires_worker', False),
            action_type=child.get('action_type', ''),
            action_payload=payload.action_payload or {},
        )
        child_task = create_task(db, child_payload)
        child_task.parent_task_id = task.id
        child_task.execution_blocked = True
        child_task.status = 'draft'
        db.commit(); db.refresh(child_task)
        create_approval(db, child_task.id, f"Approval required before execution for child task {child_task.title}")
        created_children.append(child_task.id)
    create_approval(db, task.id, f"Approval required before execution for task {task.title}")
    db.refresh(task)
    return {
        "id": task.id, "status": task.status, "location": task.location,
        "draft_output": task.draft_output, "evaluation": task.evaluation_json,
        "execution_blocked": task.execution_blocked, "child_task_ids": created_children,
    }

@router.get("")
def list_tasks(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Task).order_by(Task.created_at.desc()).all()
    return [{"id": r.id, "title": r.title, "status": r.status, "location": r.location, "priority": r.priority, "runtime_note": r.runtime_note, "parent_task_id": r.parent_task_id} for r in rows]

@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    try:
        evaluation = json.loads(task.evaluation_json or '{}')
    except Exception:
        evaluation = {}
    children = db.query(Task).filter(Task.parent_task_id == task.id).order_by(Task.created_at.asc()).all()
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "location": task.location,
        "priority": task.priority,
        "draft_output": task.draft_output,
        "final_output": task.final_output,
        "evaluation": evaluation,
        "runtime_note": task.runtime_note,
        "execution_blocked": task.execution_blocked,
        "child_tasks": [{"id": c.id, "title": c.title, "status": c.status} for c in children],
    }

@router.patch("/{task_id}")
def patch_task(task_id: int, payload: TaskUpdateRequest, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "operator"]))):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if payload.status:
        update_task_status(db, task, payload.status)
    if payload.assigned_to is not None:
        task.assigned_to = payload.assigned_to
    if payload.location is not None:
        task.location = payload.location
    db.commit()
    db.refresh(task)
    return {"id": task.id, "status": task.status, "assigned_to": task.assigned_to, "location": task.location}

@router.get("/{task_id}/steps")
def task_steps(task_id: int, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    steps = db.query(TaskStep).filter(TaskStep.task_id == task_id).order_by(TaskStep.order_index.asc()).all()
    return [{"id": s.id, "title": s.title, "agent_name": s.agent_name, "status": s.status, "order_index": s.order_index, "decision_note": s.decision_note} for s in steps]

@router.post("/{task_id}/execute")
def execute_task(task_id: int, payload: TaskExecutionRequest, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver"]))):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if payload.approved and task.execution_blocked:
        task.execution_blocked = False
        task.status = 'approved'
        db.commit()
        db.refresh(task)
    return execute_task_if_approved(db, task)
