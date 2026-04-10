from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..auth import require_role
from ..database import get_db
from ..device_control import wake_device
from ..models import Device, Command

router = APIRouter(prefix="/api/runtime", tags=["runtime"])

@router.post("/devices/{device_id}/wake")
def wake(device_id: str, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "operator"]))):
    device = db.query(Device).filter(or_(Device.device_id == device_id, Device.id == int(device_id) if device_id.isdigit() else -1)).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    result = wake_device(db, device)
    cmd = Command(device_id=device.id, target_kind='device', command_type="wake_pc", command_text="wake", status=result["status"], result=str(result))
    db.add(cmd)
    db.commit()
    return result
