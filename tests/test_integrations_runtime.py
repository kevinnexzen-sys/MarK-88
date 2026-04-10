from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def auth():
    r = client.post('/api/auth/login', json={'username':'admin','password':'admin123'})
    return {'Authorization': f"Bearer {r.json()['token']}"}


def test_whatsapp_queue_without_worker_fails_or_queues():
    headers = auth()
    client.post('/api/workers/register', json={'worker_id':'w1','name':'Worker','worker_type':'desktop','capabilities':{'whatsapp':True}})
    r = client.post('/api/integrations/whatsapp/queue', json={'command_type':'whatsapp_send','payload':{'phone':'15551234567','message':'hello'}}, headers=headers)
    assert r.status_code == 200
    assert r.json()['status'] == 'queued'


def test_task_cloud_noop_action():
    headers = auth()
    task = client.post('/api/tasks', json={'title':'noop task','description':'x','action_type':'unknown_action','action_payload':{}}, headers=headers).json()
    task_id = task['id']
    client.post(f'/api/tasks/{task_id}/execute', json={'approved': True}, headers=headers)
    detail = client.get(f'/api/tasks/{task_id}', headers=headers).json()
    assert detail['status'] in ('completed','approved','executing')
