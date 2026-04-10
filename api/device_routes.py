import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Device, Command
from ..schemas import DeviceRegisterRequest, DeviceCommandRequest
from ..auth import require_role
from ..runtime_executor import complete_command
from ..device_control import wake_device

router = APIRouter(prefix="/api/devices", tags=["devices"])

@router.post("/register")
def register(payload: DeviceRegisterRequest, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == payload.device_id).first()
    if not device:
        device = Device(device_id=payload.device_id, name=payload.name, device_type=payload.device_type)
        db.add(device)
    device.mac = payload.mac
    device.status = "online"
    device.last_seen = datetime.utcnow()
    device.online_method = payload.online_method
    device.smart_plug_json = json.dumps(payload.smart_plug or {})
    db.commit(); db.refresh(device)
    return {"status": "ok", "device_id": device.device_id, 'id': device.id}

@router.post('/{device_id}/heartbeat')
def device_heartbeat(device_id: str, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail='Device not found')
    device.status = 'online'; device.last_seen = datetime.utcnow(); db.commit()
    return {"status": "ok", "last_seen": device.last_seen.isoformat()}

@router.get("")
def list_devices(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    rows = db.query(Device).all()
    return [{"id": r.id, "device_id": r.device_id, "name": r.name, "status": r.status, "last_seen": r.last_seen.isoformat() if r.last_seen else None, "mac": r.mac, "method": r.online_method} for r in rows]

@router.get("/{device_id}")
def get_device(device_id: str, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    r = db.query(Device).filter(Device.device_id == device_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"id": r.id, "device_id": r.device_id, "name": r.name, "status": r.status, "mac": r.mac, "method": r.online_method}

@router.post("/{device_id}/command")
def create_device_command(device_id: str, payload: DeviceCommandRequest, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "operator"]))):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    cmd = Command(device_id=device.id, target_kind='device', command_type=payload.command_type, command_text=payload.command_text, status="pending")
    db.add(cmd); db.commit(); db.refresh(cmd)
    return {"status": "queued", "command_id": cmd.id}

@router.get('/{device_id}/commands')
def poll_device_commands(device_id: str, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail='Device not found')
    cmds = db.query(Command).filter(Command.device_id == device.id, Command.status == 'pending').order_by(Command.created_at.asc()).all()
    out=[]
    for c in cmds:
        try:
            payload = json.loads(c.payload_json or '{}')
        except Exception:
            payload = {}
        out.append({"id": c.id, "command_type": c.command_type, "command_text": c.command_text, "payload": payload, "task_id": c.task_id})
    return out

@router.post('/{device_id}/commands/{command_id}/complete')
def complete_device_command(device_id: str, command_id: int, payload: dict, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail='Device not found')
    cmd = db.query(Command).filter(Command.id == command_id, Command.device_id == device.id).first()
    if not cmd:
        raise HTTPException(status_code=404, detail='Command not found')
    complete_command(db, cmd, payload.get('result', ''), payload.get('status', 'completed'))
    return {"status": "ok"}

@router.post('/{device_id}/wake')
def wake_alias(device_id: str, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "operator"]))):
    device = db.query(Device).filter(or_(Device.device_id == device_id, Device.id == int(device_id) if device_id.isdigit() else -1)).first()
    if not device:
        raise HTTPException(status_code=404, detail='Device not found')
    return wake_device(db, device)
