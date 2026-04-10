from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import require_role
from ..voice_policy import get_voice_policy
from ..command_parser import interpret_command

router = APIRouter(prefix="/api/voice", tags=["voice"])

@router.get("/policy")
def policy(_=Depends(require_role(["admin","manager","approver","operator","viewer"]))):
    return get_voice_policy()

@router.post("/interpret")
def interpret(payload: dict, db: Session = Depends(get_db), _=Depends(require_role(["admin","manager","approver","operator"]))):
    parsed = interpret_command(payload.get("text",""))
    voice_reply = f"I understood this as: {parsed['title']}. I will prepare it as a draft for your approval."
    return {"parsed": parsed, "voice_reply": voice_reply, "speak_on_mobile_only": True}
