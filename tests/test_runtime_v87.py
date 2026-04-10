from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_voice_and_runtime_tick():
    r = client.post('/api/auth/login', json={'username':'admin','password':'admin123'})
    assert r.status_code == 200
    token = r.json()['token']
    headers = {'Authorization': f'Bearer {token}'}
    r = client.post('/api/commands/interpret', headers=headers, json={'text':'wake pc and prepare browser task'})
    assert r.status_code == 200
    task_id = r.json()['task_id']
    r = client.post(f'/api/approvals/task/{task_id}/approve', headers=headers)
    assert r.status_code == 200
    r = client.post('/api/runtime/tick', headers=headers)
    assert r.status_code == 200
