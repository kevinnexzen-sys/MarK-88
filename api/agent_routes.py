from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Agent, TaskStep, Task
from ..agents.subagent_registry import choose_templates

router = APIRouter(prefix='/api/agents', tags=['agents'])

@router.get('')
def list_agents(db: Session = Depends(get_db)):
    return [
        {
            'id': a.id,
            'name': a.name,
            'role': a.role,
            'status': a.status,
            'scope': a.scope,
            'autonomy_level': a.autonomy_level,
        } for a in db.query(Agent).order_by(Agent.name.asc()).all()
    ]

@router.get('/task/{task_id}/subagents')
def task_subagents(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        return []
    templates = choose_templates(task.title)
    steps = db.query(TaskStep).filter(TaskStep.task_id == task_id).order_by(TaskStep.order_index.asc()).all()
    return {
        'templates': templates,
        'steps': [
            {'title': s.title, 'agent_name': s.agent_name, 'status': s.status, 'decision_note': s.decision_note}
            for s in steps
        ]
    }
