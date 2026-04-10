import json
from .models import Device, Command
from .integrations.smart_plug import turn_on_plug
from .wake_relay import send_wol


def queue_power_command(db, device: Device, command_type: str, payload: dict | None = None):
    cmd = Command(device_id=device.id, target_kind='device', command_type=command_type, payload_json=json.dumps(payload or {}), status='pending')
    db.add(cmd)
    db.commit()
    db.refresh(cmd)
    return cmd


def wake_device(db, device: Device):
    if device.status == 'online':
        return {'status': 'already_online', 'device_id': device.device_id}
    if device.mac:
        try:
            send_wol(device.mac)
            return {'status': 'wake_sent', 'method': 'wol', 'device_id': device.device_id}
        except Exception:
            pass
    try:
        plug = json.loads(device.smart_plug_json or '{}')
    except Exception:
        plug = {}
    if plug:
        result = turn_on_plug(plug)
        return {'status': 'wake_sent', 'method': 'smart_plug', 'detail': result, 'device_id': device.device_id}
    return {'status': 'failed', 'reason': 'no_wake_method', 'device_id': device.device_id}
