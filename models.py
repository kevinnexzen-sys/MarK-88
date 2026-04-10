from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, Boolean, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

def utcnow():
    return datetime.utcnow()

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow)

class Role(Base, TimestampMixin):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)

class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    role_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship()

class SessionToken(Base, TimestampMixin):
    __tablename__ = "session_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    user: Mapped["User"] = relationship()

class Task(Base, TimestampMixin):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default="")
    source: Mapped[str] = mapped_column(String(50), default="dashboard")
    status: Mapped[str] = mapped_column(String(50), default="pending")
    location: Mapped[str] = mapped_column(String(50), default="cloud")
    priority: Mapped[int] = mapped_column(Integer, default=5)
    assigned_to: Mapped[str] = mapped_column(String(80), default="CEO")
    requested_by: Mapped[str] = mapped_column(String(80), default="user")
    project_key: Mapped[str] = mapped_column(String(120), default="default")
    provider_mode: Mapped[str] = mapped_column(String(30), default="balanced")
    requires_online: Mapped[bool] = mapped_column(Boolean, default=False)
    requires_worker: Mapped[bool] = mapped_column(Boolean, default=False)
    parent_task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id"), nullable=True)
    draft_output: Mapped[str] = mapped_column(Text, default="")
    final_output: Mapped[str] = mapped_column(Text, default="")
    evaluation_json: Mapped[str] = mapped_column(Text, default="{}")
    execution_blocked: Mapped[bool] = mapped_column(Boolean, default=True)
    estimated_time_saved_minutes: Mapped[int] = mapped_column(Integer, default=0)
    estimated_value_usd: Mapped[int] = mapped_column(Integer, default=0)
    runtime_note: Mapped[str] = mapped_column(Text, default="")
    action_type: Mapped[str] = mapped_column(String(80), default="")
    action_payload_json: Mapped[str] = mapped_column(Text, default="{}")

class TaskStep(Base, TimestampMixin):
    __tablename__ = "task_steps"
    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    parent_step_id: Mapped[int | None] = mapped_column(ForeignKey("task_steps.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    agent_name: Mapped[str] = mapped_column(String(80), default="PlannerAgent")
    status: Mapped[str] = mapped_column(String(50), default="pending")
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    decision_note: Mapped[str] = mapped_column(Text, default="")
    task: Mapped["Task"] = relationship()

class Approval(Base, TimestampMixin):
    __tablename__ = "approvals"
    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    requested_for: Mapped[str] = mapped_column(String(80), default="approver")
    status: Mapped[str] = mapped_column(String(50), default="pending")
    summary: Mapped[str] = mapped_column(Text, default="")
    response_note: Mapped[str] = mapped_column(Text, default="")

class Agent(Base, TimestampMixin):
    __tablename__ = "agents"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    role: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(50), default="active")
    scope: Mapped[str] = mapped_column(Text, default="")
    autonomy_level: Mapped[str] = mapped_column(String(30), default="balanced")
    capabilities_json: Mapped[str] = mapped_column(Text, default="{}")

class Worker(Base, TimestampMixin):
    __tablename__ = "workers"
    id: Mapped[int] = mapped_column(primary_key=True)
    worker_id: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(50), default="offline")
    worker_type: Mapped[str] = mapped_column(String(50), default="desktop")
    last_seen: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    capabilities_json: Mapped[str] = mapped_column(Text, default="{}")
    command_cursor: Mapped[int] = mapped_column(Integer, default=0)

class Device(Base, TimestampMixin):
    __tablename__ = "devices"
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    mac: Mapped[str] = mapped_column(String(50), default="")
    device_type: Mapped[str] = mapped_column(String(50), default="windows")
    status: Mapped[str] = mapped_column(String(50), default="offline")
    last_seen: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    online_method: Mapped[str] = mapped_column(String(50), default="wol")
    smart_plug_json: Mapped[str] = mapped_column(Text, default="{}")
    amt_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    command_cursor: Mapped[int] = mapped_column(Integer, default=0)

class Command(Base, TimestampMixin):
    __tablename__ = "commands"
    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id"), nullable=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"), nullable=True)
    worker_id: Mapped[int | None] = mapped_column(ForeignKey("workers.id"), nullable=True)
    target_kind: Mapped[str] = mapped_column(String(20), default="worker")
    command_type: Mapped[str] = mapped_column(String(50))
    command_text: Mapped[str] = mapped_column(Text, default="")
    payload_json: Mapped[str] = mapped_column(Text, default="{}")
    status: Mapped[str] = mapped_column(String(50), default="pending")
    result: Mapped[str] = mapped_column(Text, default="")

class MemoryEntry(Base, TimestampMixin):
    __tablename__ = "memory_entries"
    id: Mapped[int] = mapped_column(primary_key=True)
    entry_type: Mapped[str] = mapped_column(String(50), default="general")
    project_key: Mapped[str] = mapped_column(String(120), default="default")
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    tags: Mapped[str] = mapped_column(Text, default="")

class Skill(Base, TimestampMixin):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    version: Mapped[str] = mapped_column(String(40), default="1.0.0")
    status: Mapped[str] = mapped_column(String(50), default="draft")
    source: Mapped[str] = mapped_column(String(50), default="manual")
    logic: Mapped[str] = mapped_column(Text, default="")

class Automation(Base, TimestampMixin):
    __tablename__ = "automations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(50), default="suggested")
    description: Mapped[str] = mapped_column(Text, default="")
    source_pattern_id: Mapped[int | None] = mapped_column(ForeignKey("patterns.id"), nullable=True)

class LearningEvent(Base, TimestampMixin):
    __tablename__ = "learning_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(50), default="desktop")
    event_type: Mapped[str] = mapped_column(String(80))
    payload: Mapped[str] = mapped_column(Text, default="")
    confidence: Mapped[int] = mapped_column(Integer, default=50)
    project_key: Mapped[str] = mapped_column(String(120), default="default")

class Pattern(Base, TimestampMixin):
    __tablename__ = "patterns"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    fingerprint: Mapped[str] = mapped_column(String(255), index=True)
    frequency: Mapped[int] = mapped_column(Integer, default=1)
    confidence: Mapped[int] = mapped_column(Integer, default=50)

class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[str] = mapped_column(String(50), default="info")
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text, default="")
    read: Mapped[bool] = mapped_column(Boolean, default=False)

class Setting(Base, TimestampMixin):
    __tablename__ = "settings"
    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column(String(80), index=True)
    key: Mapped[str] = mapped_column(String(120), index=True)
    value: Mapped[str] = mapped_column(Text, default="")

class KnowledgeItem(Base, TimestampMixin):
    __tablename__ = "knowledge_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_key: Mapped[str] = mapped_column(String(120), default="default")
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text, default="")

class ProjectInstruction(Base, TimestampMixin):
    __tablename__ = "project_instructions"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_key: Mapped[str] = mapped_column(String(120), default="default")
    instruction: Mapped[str] = mapped_column(Text)

class Preview(Base, TimestampMixin):
    __tablename__ = "previews"
    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id"), nullable=True)
    preview_type: Mapped[str] = mapped_column(String(50), default="text")
    left_content: Mapped[str] = mapped_column(Text, default="")
    right_content: Mapped[str] = mapped_column(Text, default="")
