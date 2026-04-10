from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Task, Worker, Device, Approval, Command
from ..provider_router import ProviderRouter
from .subagent_registry import choose_templates

class CEOAgent:
    def __init__(self):
        self._last_heartbeat = datetime.utcnow()

    def heartbeat(self):
        self._last_heartbeat = datetime.utcnow()
        return self._last_heartbeat.isoformat()

    def heartbeat_status(self):
        return self._last_heartbeat.isoformat()

    def system_health(self, db: Session):
        router = ProviderRouter()
        provider = router.decide('system health check')
        return {
            'heartbeat': self.heartbeat(),
            'provider': provider.provider,
            'provider_mode': provider.mode,
            'provider_reason': provider.reason,
            'workers_online': db.query(Worker).filter(Worker.status == 'online').count(),
            'devices_online': db.query(Device).filter(Device.status == 'online').count(),
            'tasks_waiting_approval': db.query(Task).filter(Task.status.in_(['draft', 'waiting_approval', 'approved', 'executing', 'blocked'])).count(),
            'pending_commands': db.query(Command).filter(Command.status == 'pending').count(),
            'pending_approvals': db.query(Approval).filter(Approval.status == 'pending').count(),
        }

    def choose_provider(self, task: Task):
        router = ProviderRouter()
        payload = {}
        try:
            import json
            payload = json.loads(task.action_payload_json or '{}')
        except Exception:
            payload = {}
        return router.decide(task.title, mode=task.provider_mode, requires_online=task.requires_online, action_type=task.action_type, payload=payload)

    def route_task(self, task: Task):
        t = (task.title or '').lower()
        if task.requires_worker or any(k in t for k in ['browser', 'whatsapp', 'chrome']):
            return 'desktop_worker'
        if 'pc' in t or 'powershell' in (task.description or '').lower() or 'local file' in t:
            return 'pc_agent'
        return 'cloud'

    def subagents_for_task(self, task: Task):
        return choose_templates(task.title)
