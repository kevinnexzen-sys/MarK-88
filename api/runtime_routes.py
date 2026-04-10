from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import require_role
from ..autonomy_loop import autonomy_tick

router = APIRouter(prefix="/api/runtime", tags=["runtime"])

@router.post("/tick")
def tick(db: Session = Depends(get_db), _=Depends(require_role(["admin","manager","approver","operator"]))):
    return autonomy_tick(db)
