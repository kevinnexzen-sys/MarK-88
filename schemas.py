from typing import Any
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str
    role: str

class LoginResponse(BaseModel):
    token: str
    user: UserOut

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class SettingItem(BaseModel):
    group_name: str
    key: str
    value: str

class SettingsUpdateRequest(BaseModel):
    items: list[SettingItem]

class TaskCreateRequest(BaseModel):
    title: str
    description: str = ""
    source: str = "dashboard"
    priority: int = 5
    project_key: str = "default"
    provider_mode: str = "balanced"
    requires_online: bool = False
    requires_worker: bool = False
    action_type: str = ""
    action_payload: dict[str, Any] = {}

class TaskUpdateRequest(BaseModel):
    status: str | None = None
    assigned_to: str | None = None
    location: str | None = None

class WorkerRegisterRequest(BaseModel):
    worker_id: str
    name: str
    worker_type: str = "desktop"
    capabilities: dict[str, Any] = {}

class DeviceRegisterRequest(BaseModel):
    device_id: str
    name: str
    mac: str = ""
    device_type: str = "windows"
    online_method: str = "wol"
    smart_plug: dict[str, Any] = {}

class DeviceCommandRequest(BaseModel):
    command_type: str
    command_text: str = ""

class ApprovalActionRequest(BaseModel):
    status: str
    response_note: str = ""

class LearningEventRequest(BaseModel):
    source: str
    event_type: str
    payload: str = ""
    confidence: int = 50

class DashboardSummary(BaseModel):
    tasks: int
    pending_approvals: int
    workers_online: int
    devices_online: int
    notifications_unread: int
    ceo_heartbeat: str

class TaskExecutionRequest(BaseModel):
    approved: bool = False

class EvaluationOut(BaseModel):
    confidence: int
    issues: list[str]
    status: str

class FinancialStatsOut(BaseModel):
    total_tasks: int
    approved_or_better: int
    drafts_or_waiting: int
    estimated_time_saved_minutes: int
    estimated_value_usd: float


class IntegrationActionRequest(BaseModel):
    action_type: str
    payload: dict[str, Any] = {}

class WorkerBrowserCommandRequest(BaseModel):
    command_type: str
    payload: dict[str, Any] = {}
