from __future__ import annotations
from ..models import Task


class RouterAgent:
    def route(self, task: Task):
        t = (task.title or '').lower()
        if task.requires_worker or any(k in t for k in ['browser', 'whatsapp', 'chrome']):
            return 'desktop_worker'
        if any(k in t for k in ['wake pc', 'restart pc', 'shutdown pc', 'powershell', 'local file']):
            return 'pc_agent'
        return 'cloud'
