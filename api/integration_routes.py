from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import require_role
from ..database import get_db
from ..integration_runner import run_task_action
from ..integrations.google_sheets import upsert_row
from ..integrations.google_calendar import create_event
from ..integrations.google_mail import send_mail
from ..models import Task, Worker, Command
from ..schemas import IntegrationActionRequest, WorkerBrowserCommandRequest

router = APIRouter(prefix='/api/integrations', tags=['integrations'])

@router.post('/run')
def run_integration(payload: IntegrationActionRequest, db: Session = Depends(get_db), _=Depends(require_role(['admin','manager','operator']))):
    fake_task = type('TaskLike', (), {'title': payload.action_type, 'description': '', 'action_type': payload.action_type, 'action_payload_json': __import__('json').dumps(payload.payload)})
    result = run_task_action(db, fake_task)
    if result is None:
        raise HTTPException(status_code=400, detail='Unknown integration action')
    return result

@router.post('/whatsapp/queue')
def queue_whatsapp(payload: WorkerBrowserCommandRequest, db: Session = Depends(get_db), _=Depends(require_role(['admin','manager','operator']))):
    worker = db.query(Worker).filter(Worker.status == 'online').order_by(Worker.last_seen.desc()).first()
    if not worker:
        raise HTTPException(status_code=400, detail='No online worker available')
    cmd = Command(worker_id=worker.id, target_kind='worker', command_type=payload.command_type, payload_json=__import__('json').dumps(payload.payload), status='pending')
    db.add(cmd)
    db.commit()
    db.refresh(cmd)
    return {'status': 'queued', 'command_id': cmd.id, 'worker_id': worker.worker_id}


from ..models import KnowledgeItem
from ..learning.watch_to_learn import record_watch_batch

@router.post('/whatsapp-intake')
def whatsapp_intake(payload: dict, db: Session = Depends(get_db)):
    messages = payload.get('messages', [])
    events = []
    for m in messages:
        body = m.get('text','')
        events.append({'source': 'whatsapp', 'event_type': 'message', 'payload': body[:500], 'confidence': 72})
        if 'work order' in body.lower() or 'estimate' in body.lower():
            db.add(KnowledgeItem(project_key='default', title='WhatsApp intake', body=body[:2000]))
    record_watch_batch(db, 'whatsapp', events, 'default')
    return {'status': 'ok', 'messages': len(messages)}
