import json
from sqlalchemy.orm import Session
from .models import Task, Worker, Device, Command, Notification, TaskStep
from .self_evaluator import evaluate_task_output, dumps_eval
from .learning.watch_to_learn import record_watch_event
from .integration_runner import run_task_action
from .provider_router import ProviderRouter
from .agents.subagent_registry import choose_templates


def _cloud_output(task: Task, provider_note: str) -> str:
    base = task.draft_output or f"Draft prepared for {task.title}"
    base += f"\n\n[Provider] {provider_note}"
    return base


def queue_runtime_command(db: Session, task: Task, target: str) -> Command | None:
    payload = {
        'task_id': task.id,
        'title': task.title,
        'description': task.description,
        'action_type': task.action_type,
        'action_payload': json.loads(task.action_payload_json or '{}'),
    }
    if target == 'desktop_worker':
        worker = db.query(Worker).filter(Worker.status == 'online').order_by(Worker.last_seen.desc()).first()
        if not worker:
            task.status = 'blocked'
            task.runtime_note = 'No online desktop worker available.'
            db.add(Notification(level='warning', title='Task blocked', content=f'{task.title} is waiting for a desktop worker.'))
            db.commit()
            return None
        cmd = Command(task_id=task.id, worker_id=worker.id, target_kind='worker', command_type='execute_task', payload_json=json.dumps(payload), status='pending')
        db.add(cmd)
        task.status = 'executing'
        task.runtime_note = f'Queued to worker {worker.worker_id}'
        db.commit()
        db.refresh(cmd)
        return cmd
    if target == 'pc_agent':
        device = db.query(Device).filter(Device.status == 'online').order_by(Device.last_seen.desc()).first()
        if not device:
            task.status = 'blocked'
            task.runtime_note = 'No online PC agent available.'
            db.add(Notification(level='warning', title='Task blocked', content=f'{task.title} is waiting for a PC agent.'))
            db.commit()
            return None
        cmd = Command(task_id=task.id, device_id=device.id, target_kind='device', command_type='execute_task', payload_json=json.dumps(payload), status='pending')
        db.add(cmd)
        task.status = 'executing'
        task.runtime_note = f'Queued to device {device.device_id}'
        db.commit()
        db.refresh(cmd)
        return cmd
    return None


def execute_task_if_approved(db: Session, task: Task) -> dict:
    if task.execution_blocked:
        return {'status': 'blocked', 'reason': 'approval_required'}
    router = ProviderRouter()
    payload = json.loads(task.action_payload_json or '{}')
    decision = router.decide(task.title, mode=task.provider_mode, requires_online=task.requires_online, action_type=task.action_type, payload=payload)
    target = task.location or 'cloud'
    subagents = choose_templates(task.title)
    task.runtime_note = f'Subagents: {", ".join(subagents)} | Provider: {decision.provider}/{decision.mode}'
    if target == 'cloud':
        action_result = run_task_action(db, task)
        base = _cloud_output(task, decision.reason)
        if action_result is not None:
            base += f"\n\n[Action result] {json.dumps(action_result)}"
        task.final_output = base
        task.status = 'completed'
        evaluation = evaluate_task_output(task.title, task.final_output)
        task.evaluation_json = dumps_eval(evaluation)
        for step in db.query(TaskStep).filter(TaskStep.task_id == task.id).all():
            step.status = 'completed'
        db.add(Notification(level='success', title='Task completed', content=f'{task.title} completed in cloud via {decision.provider}.'))
        record_watch_event(db, source='cloud', event_type='task_completed', payload=task.title, confidence=85)
        db.commit()
        db.refresh(task)
        return {'status': 'completed', 'location': 'cloud', 'task_id': task.id, 'action_result': action_result, 'provider': decision.__dict__, 'subagents': subagents}
    cmd = queue_runtime_command(db, task, target)
    if cmd is None:
        return {'status': 'blocked', 'reason': task.runtime_note, 'provider': decision.__dict__, 'subagents': subagents}
    return {'status': 'queued', 'location': target, 'command_id': cmd.id, 'task_id': task.id, 'provider': decision.__dict__, 'subagents': subagents}


def complete_command(db: Session, command: Command, result: str = '', status: str = 'completed'):
    command.status = status
    command.result = result
    task = db.get(Task, command.task_id) if command.task_id else None
    if task:
        task.status = 'completed'
        task.final_output = result or task.draft_output or f'Executed task {task.title}'
        evaluation = evaluate_task_output(task.title, task.final_output)
        task.evaluation_json = dumps_eval(evaluation)
        db.add(Notification(level='success', title='Worker result received', content=f'{task.title} completed by {command.target_kind}.'))
        record_watch_event(db, source=command.target_kind or 'worker', event_type='task_completed', payload=task.title, confidence=80)
    db.commit()
    return {'status': 'completed', 'command_id': command.id}
