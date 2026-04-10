from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..agents.ceo_agent import CEOAgent
from ..monitoring import stale_workers

router = APIRouter(tags=["health"])
ceo = CEOAgent()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/api/health/ceo")
def ceo_health(db: Session = Depends(get_db)):
    return ceo.system_health(db)

@router.get("/api/health/providers")
def provider_health():
    return {"providers": ["local", "openai", "anthropic", "gemini"], "status": "placeholder"}

@router.get("/api/health/workers")
def worker_health(db: Session = Depends(get_db)):
    return {"stale_workers": [w.worker_id for w in stale_workers(db)]}
