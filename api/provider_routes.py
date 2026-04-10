from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..provider_router import ProviderRouter
from ..settings_service import get_group_settings

router = APIRouter(prefix='/api/providers', tags=['providers'])

@router.get('/status')
def provider_status(db: Session = Depends(get_db)):
    cfg = get_group_settings(db, 'providers')
    return {
        'configured_mode': cfg.get('mode', 'balanced'),
        'available': ['local', 'openai', 'anthropic', 'gemini'],
        'fallback_chain': ['local', 'openai', 'anthropic', 'gemini'],
    }

@router.post('/decide')
def decide_provider(payload: dict):
    router = ProviderRouter()
    decision = router.decide(
        payload.get('title', ''),
        mode=payload.get('mode', 'balanced'),
        requires_online=payload.get('requires_online', False),
        action_type=payload.get('action_type', ''),
        payload=payload.get('action_payload', {}),
    )
    return decision.__dict__
