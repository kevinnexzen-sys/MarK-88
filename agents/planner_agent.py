from __future__ import annotations
from ..models import Task


class PlannerAgent:
    def build_plan(self, task: Task):
        title = (task.title or '').lower()
        steps = [
            {"title": "Understand request", "agent_name": "PlannerAgent", "decision_note": "Normalize request and infer execution strategy"},
            {"title": "Select provider and route", "agent_name": "RouterAgent", "decision_note": "Choose cloud/local/worker path"},
        ]
        if 'estimate' in title:
            steps += [
                {"title": "Spawn estimate subagents", "agent_name": "EstimateAgent", "decision_note": "Parse findings, build materials/labor, validate SOP"},
                {"title": "Validate draft", "agent_name": "SOPValidator", "decision_note": "Run SOP, pricing, contamination checks"},
                {"title": "Prepare approval package", "agent_name": "ApprovalGatekeeper", "decision_note": "Attach evaluation and draft output"},
            ]
        elif any(k in title for k in ['sheet', 'email', 'calendar', 'work order']):
            steps += [
                {"title": "Spawn integration subagents", "agent_name": "RouterAgent", "decision_note": "Decompose into sheet/email/calendar actions"},
                {"title": "Prepare approval package", "agent_name": "ApprovalGatekeeper"},
            ]
        elif any(k in title for k in ['code', 'app', 'preview']):
            steps += [
                {"title": "Spawn codegen subagents", "agent_name": "CodegenAgent", "decision_note": "Generate, preview, and review output"},
                {"title": "Prepare preview package", "agent_name": "ApprovalGatekeeper"},
            ]
        else:
            steps += [
                {"title": "Spawn general specialist", "agent_name": "RouterAgent", "decision_note": "Choose specialist agent template"},
                {"title": "Prepare approval package", "agent_name": "ApprovalGatekeeper"},
            ]
        return {"steps": steps, "subtasks": self.suggest_subtasks(task)}

    def suggest_subtasks(self, task: Task):
        title = (task.title or '').lower()
        subtasks = []
        if any(k in title for k in ['estimate', 'invoice', 'sheet', 'email', 'calendar', 'whatsapp', 'browser']):
            if 'estimate' in title:
                subtasks.extend([
                    {"title": f"Parse source for {task.title}", "location": task.location, "action_type": "analyze", "requires_online": False},
                    {"title": f"Draft output for {task.title}", "location": task.location, "action_type": task.action_type or 'draft_text', "requires_online": task.requires_online},
                ])
            if any(k in title for k in ['sheet', 'email', 'calendar']):
                subtasks.append({"title": f"Integration action for {task.title}", "location": 'cloud', "action_type": task.action_type or 'integration', "requires_online": True})
            if any(k in title for k in ['whatsapp', 'browser']):
                subtasks.append({"title": f"Worker action for {task.title}", "location": 'desktop_worker', "action_type": task.action_type or 'browser_open', "requires_online": True, "requires_worker": True})
        if len(subtasks) < 2:
            return []
        return subtasks[:3]
