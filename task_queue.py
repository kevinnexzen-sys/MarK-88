import json
from sqlalchemy.orm import Session
from .models import Task, TaskStep
from .schemas import TaskCreateRequest
from .agents.planner_agent import PlannerAgent
from .agents.router_agent import RouterAgent
from .self_evaluator import evaluate_task_output, dumps_eval
from .financial_tracker import estimate_financials
from .approvals import create_approval_for_task

VALID_STATUSES = {"draft", "pending", "planned", "ready_for_review", "waiting_approval", "approved", "executing", "running", "completed", "failed", "blocked", "rejected"}

def create_task(db: Session, payload: TaskCreateRequest) -> Task:
    task = Task(
        title=payload.title,
        description=payload.description,
        source=payload.source,
        status="draft",
        priority=payload.priority,
        project_key=payload.project_key,
        provider_mode=payload.provider_mode,
        requires_online=payload.requires_online,
        requires_worker=payload.requires_worker,
        action_type=payload.action_type,
        action_payload_json=json.dumps(payload.action_payload or {}),
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    planner = PlannerAgent()
    plan = planner.build_plan(task)
    for idx, step in enumerate(plan["steps"]):
        db.add(TaskStep(
            task_id=task.id,
            title=step["title"],
            agent_name=step.get("agent_name", "PlannerAgent"),
            order_index=idx,
            decision_note=step.get("decision_note", ""),
        ))
    task.status = "planned"
    router = RouterAgent()
    task.location = router.route(task)
    task.draft_output = f"Draft prepared for: {task.title}\n\nDescription: {task.description or 'No description provided.'}\nExecution target: {task.location}"
    evaluation = evaluate_task_output(task.title, task.draft_output)
    task.evaluation_json = dumps_eval(evaluation)
    task.status = "waiting_approval"
    task.execution_blocked = True
    financials = estimate_financials(task)
    task.estimated_time_saved_minutes = financials["estimated_time_saved_minutes"]
    task.estimated_value_usd = int(round(financials["estimated_value_usd"]))
    db.commit()
    create_approval_for_task(db, task.id, f"Approve task: {task.title}")
    db.refresh(task)
    return task

def update_task_status(db: Session, task: Task, new_status: str):
    if new_status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {new_status}")
    task.status = new_status
    db.commit()
    create_approval_for_task(db, task.id, f"Approve task: {task.title}")
    db.refresh(task)
    return task
