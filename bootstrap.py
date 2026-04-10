from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .config import DEFAULT_ROLES, DEFAULT_USERS, SETTING_GROUPS, DEFAULT_PROVIDER_MODE
from .models import Role, User, Setting, Agent
from .auth import hash_password

DEFAULT_SETTINGS = {
    "general": {
        "app_name": "MARK v8.1",
        "project_mode": "cloud_first",
    },
    "providers": {
        "mode": DEFAULT_PROVIDER_MODE,
        "primary_provider": "local",
        "fallback_provider": "openai",
    },
    "supabase": {
        "url": "",
        "anon_key": "",
        "service_key": "",
    },
    "google": {
        "service_account_json": "",
        "sheet_id": "",
        "calendar_id": "",
        "gmail_sender": "",
    },
    "voice": {
        "mobile_voice_enabled": "true",
        "desktop_speak_enabled": "false",
        "voice_style": "natural",
    },
    "device_control": {
        "wol_enabled": "true",
        "smart_plug_enabled": "true",
        "amt_enabled": "false",
    },
    "whatsapp": {
        "approval_mode": "true",
        "selected_groups": "",
    },
}

DEFAULT_AGENTS = [
    ("CEO", "Master Controller"),
    ("PlannerAgent", "Task Graph Builder"),
    ("RouterAgent", "Cloud/Desktop/Mobile Router"),
    ("MemoryAgent", "Persistent Memory"),
    ("WatchToLearnAgent", "Workflow Observer"),
    ("SearchToSkillAgent", "Search Learning"),
    ("PatternDetectionAgent", "Pattern Detector"),
    ("AutomationSuggestionAgent", "Automation Proposer"),
    ("EstimateAgent", "Estimate Writer"),
    ("InvoiceAgent", "Invoice Builder"),
    ("SheetsAgent", "Google Sheets"),
    ("EmailAgent", "Email Actions"),
    ("CalendarAgent", "Calendar Actions"),
    ("WhatsAppAgent", "WhatsApp Operations"),
    ("CodeGenAgent", "Code/App Generator"),
    ("SOPValidator", "Estimate SOP Validator"),
    ("PricingValidator", "Pricing Validator"),
    ("ContaminationChecker", "Cross-job Checker"),
    ("ApprovalGatekeeper", "Approval Gate"),
]

def seed_defaults(db: Session):
    roles = {r.name: r for r in db.query(Role).all()}
    for name in DEFAULT_ROLES:
        if name not in roles:
            db.add(Role(name=name))
    db.commit()
    roles = {r.name: r for r in db.query(Role).all()}

    for username, password, role_name in DEFAULT_USERS:
        exists = db.query(User).filter(User.username == username).first()
        if not exists:
            db.add(User(username=username, password_hash=hash_password(password), role_id=roles[role_name].id))
    db.commit()

    existing = {(s.group_name, s.key) for s in db.query(Setting).all()}
    for group_name, items in DEFAULT_SETTINGS.items():
        for key, value in items.items():
            if (group_name, key) not in existing:
                db.add(Setting(group_name=group_name, key=key, value=value))
    db.commit()

    known_agents = {a.name for a in db.query(Agent).all()}
    for name, role in DEFAULT_AGENTS:
        if name not in known_agents:
            db.add(Agent(name=name, role=role, status="active", scope="system", autonomy_level="balanced"))
    db.commit()
