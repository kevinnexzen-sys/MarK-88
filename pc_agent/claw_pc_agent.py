from __future__ import annotations
import os, time, subprocess, requests

BASE_URL = os.getenv('MARK_BASE_URL', 'http://127.0.0.1:8787')
DEVICE_ID = os.getenv('DEVICE_ID', 'win-pc-01')
TOKEN = os.getenv('MARK_TOKEN', '')


def headers():
    h = {'Content-Type': 'application/json'}
    if TOKEN:
        h['Authorization'] = f'Bearer {TOKEN}'
    return h


def register():
    payload = {'device_id': DEVICE_ID, 'name': DEVICE_ID, 'status': 'online', 'type': 'windows'}
    return requests.post(f'{BASE_URL}/api/devices/register', headers=headers(), json=payload, timeout=10).json()


def heartbeat():
    try:
        requests.post(f'{BASE_URL}/api/devices/{DEVICE_ID}/heartbeat', headers=headers(), timeout=10)
    except Exception:
        pass


def poll():
    try:
        r = requests.get(f'{BASE_URL}/api/devices/{DEVICE_ID}/commands', headers=headers(), timeout=20)
        return r.json()
    except Exception:
        return []


def complete(cmd_id: int, result: str):
    try:
        requests.post(f'{BASE_URL}/api/devices/commands/{cmd_id}/complete', headers=headers(), json={'result': result}, timeout=20)
    except Exception:
        pass


def handle(cmd: dict) -> str:
    payload = cmd.get('payload', {})
    ctype = cmd.get('command_type')
    if ctype == 'restart_device':
        return 'Restart requested (stub)'
    if ctype == 'shutdown_device':
        return 'Shutdown requested (stub)'
    if ctype == 'wake_device':
        return 'Wake acknowledged by device agent'
    if ctype == 'execute_task':
        action = payload.get('action_type', '')
        if action == 'powershell':
            ps = payload.get('action_payload', {}).get('script', 'Write-Output "Hello from MARK"')
            try:
                out = subprocess.check_output(['powershell', '-Command', ps], stderr=subprocess.STDOUT, timeout=20)
                return out.decode(errors='ignore')[:1000]
            except Exception as e:
                return f'powershell failed: {e}'
        return f"pc task executed | title={payload.get('title')}"
    if ctype == 'shutdown':
        return 'shutdown requested (simulated)'
    if ctype == 'restart':
        return 'restart requested (simulated)'
    return f'unknown command type={ctype}'


if __name__ == '__main__':
    register()
    while True:
        heartbeat()
        for cmd in poll() or []:
            result = handle(cmd)
            complete(cmd['id'], result)
        time.sleep(5)
