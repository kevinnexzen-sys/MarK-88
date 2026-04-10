from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import SettingsUpdateRequest
from ..settings_service import get_all_settings, get_group_settings, put_settings
from ..auth import require_role

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("")
def get_settings(db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver"]))):
    return get_all_settings(db)

@router.put("")
def update_settings(payload: SettingsUpdateRequest, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager"]))):
    return put_settings(db, payload.items)

@router.get("/groups/{group_name}")
def get_group(group_name: str, db: Session = Depends(get_db), _=Depends(require_role(["admin", "manager", "approver", "operator", "viewer"]))):
    return get_group_settings(db, group_name)
