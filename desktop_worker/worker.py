from __future__ import annotations
import json, os, time, requests
from whatsapp_bridge import parse_whatsapp_message

BASE_URL = os.environ.get('MARK_BASE_URL', 'http://127.0.0.1:8787')
WORKER_ID = os.environ.get('MARK_WORKER_ID', 'desktop-worker-01')
CAPABILITIES = {
    'whatsapp': True,
    'browser': True,
    'local_watch': True,
    'ocr': True,
    'voice_listen': True,
    'local_execution': True,
}


def post(path, payload):
    return requests.post(f"{BASE_URL}{path}", json=payload, timeout=30)


def get(path):
    return requests.get(f"{BASE_URL}{path}", timeout=30)


def register():
    post('/api/workers/register', {'worker_id': WORKER_ID, 'name': 'Desktop Worker', 'worker_type': 'desktop', 'capabilities': CAPABILITIES})


def heartbeat():
    post('/api/workers/heartbeat', {'worker_id': WORKER_ID, 'capabilities': CAPABILITIES})


def emit_learning(event_type, payload, confidence=65):
    try:
        post('/api/learning/desktop-event', {'event_type': event_type, 'payload': payload, 'confidence': confidence})
    except Exception:
        pass


def handle_command(cmd):
    ctype = cmd.get('command_type')
    payload = cmd.get('payload', {}) or {}
    result = ''
    status = 'completed'
    if ctype == 'execute_task':
        title = payload.get('title', 'task')
        action_type = payload.get('action_type', '')
        emit_learning('worker_execute_task', title, 78)
        if action_type == 'whatsapp_send':
            message = payload.get('action_payload', {}).get('text', f'Approved response for {title}')
            result = f'Prepared WhatsApp send: {message}'
        elif action_type == 'browser_open':
            url = payload.get('action_payload', {}).get('url', 'https://web.whatsapp.com')
            result = f'Browser open requested: {url}'
        else:
            result = f'Worker executed task: {title}'
    elif ctype == 'whatsapp_send':
        text = payload.get('text', '')
        parsed = parse_whatsapp_message(text)
        emit_learning('whatsapp_command', text[:200], 70)
        result = f"WhatsApp send prepared ({parsed.get('intent')}): {text}"
    elif ctype == 'browser_open':
        url = payload.get('url', '')
        emit_learning('browser_open', url, 60)
        result = f'Browser open prepared: {url}'
    else:
        status = 'failed'
        result = f'Unknown command type: {ctype}'
    post(f"/api/workers/{WORKER_ID}/commands/{cmd['id']}/complete", {'result': result, 'status': status})


def poll_once():
    r = get(f'/api/workers/{WORKER_ID}/commands')
    for cmd in r.json():
        handle_command(cmd)


if __name__ == '__main__':
    register()
    while True:
        try:
            heartbeat()
            poll_once()
        except Exception:
            pass
        time.sleep(5)
