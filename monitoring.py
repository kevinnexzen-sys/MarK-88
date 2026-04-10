from datetime import datetime
from sqlalchemy.orm import Session
from .models import Worker, Device, Task, Approval, Notification, Command


def dashboard_summary(db: Session, ceo_heartbeat: str):
    return {
        "tasks": db.query(Task).count(),
        "pending_approvals": db.query(Approval).filter(Approval.status == "pending").count(),
        "workers_online": db.query(Worker).filter(Worker.status == "online").count(),
        "devices_online": db.query(Device).filter(Device.status == "online").count(),
        "notifications_unread": db.query(Notification).filter(Notification.read == False).count(),  # noqa: E712
        "pending_commands": db.query(Command).filter(Command.status == 'pending').count(),
        "ceo_heartbeat": ceo_heartbeat,
    }


def stale_workers(db: Session, max_age_seconds: int = 60):
    now = datetime.utcnow()
    items = []
    for worker in db.query(Worker).all():
        if worker.last_seen and (now - worker.last_seen).total_seconds() > max_age_seconds:
            items.append(worker)
    return items


def stale_devices(db: Session, max_age_seconds: int = 60):
    now = datetime.utcnow()
    items = []
    for device in db.query(Device).all():
        if device.last_seen and (now - device.last_seen).total_seconds() > max_age_seconds:
            items.append(device)
    return items
