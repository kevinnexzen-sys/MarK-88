from pathlib import Path
import os, tempfile

APP_NAME = "MARK v8.2"
APP_VERSION = "8.2.0"
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("MARK_DATA_DIR", tempfile.gettempdir())) / "mark_v8_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "mark_v8.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

DEFAULT_PROVIDER_MODE = "balanced"
PROVIDER_MODES = ["fast", "balanced", "privacy"]
SUPPORTED_PROVIDERS = ["openai", "anthropic", "gemini", "local"]

DEFAULT_ROLES = ["admin", "manager", "approver", "operator", "viewer"]
DEFAULT_USERS = [
    ("admin", "admin123", "admin"),
    ("manager", "manager123", "manager"),
    ("approver", "approver123", "approver"),
]

SETTING_GROUPS = [
    "general",
    "providers",
    "supabase",
    "google",
    "voice",
    "device_control",
    "whatsapp",
]

VOICE_POLICY = {
    "desktop_listen_only": True,
    "mobile_speak_enabled": True,
    "speak_only_on_mobile": True,
    "desktop_silent_updates": True,
}

WORKER_DEFAULT_CAPABILITIES = {
    "whatsapp": False,
    "browser": False,
    "local_watch": False,
    "ocr": False,
    "voice_listen": False,
    "local_execution": False,
}
