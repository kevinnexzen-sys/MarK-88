from sqlalchemy.orm import Session
from .models import Task

def estimate_financials(task: Task) -> dict:
    title = (task.title or '').lower()
    base_minutes = 15
    if any(k in title for k in ['estimate', 'invoice', 'sheet', 'calendar', 'email']):
        base_minutes = 25
    if any(k in title for k in ['automation', 'workflow', 'batch']):
        base_minutes = 45
    value = round((base_minutes / 60.0) * 35.0, 2)
    return {"estimated_time_saved_minutes": base_minutes, "estimated_value_usd": value}

def portfolio_stats(db: Session) -> dict:
    tasks = db.query(Task).all()
    total_minutes = sum(t.estimated_time_saved_minutes or 0 for t in tasks)
    total_value = round(sum(float(t.estimated_value_usd or 0) for t in tasks), 2)
    approved = sum(1 for t in tasks if t.status in ['approved', 'executing', 'completed'])
    drafts = sum(1 for t in tasks if t.status in ['draft', 'ready_for_review', 'waiting_approval'])
    return {
        "total_tasks": len(tasks),
        "approved_or_better": approved,
        "drafts_or_waiting": drafts,
        "estimated_time_saved_minutes": total_minutes,
        "estimated_value_usd": total_value,
    }
