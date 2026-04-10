# MARK v8 Capability Cross-Check

Each locked capability is represented in code or reserved with a dedicated module/file so it cannot disappear during iteration.

## Core AI + agent system
- CEO heartbeat: `backend/app/agents/ceo_agent.py`
- Planner: `backend/app/agents/planner_agent.py`
- Router: `backend/app/agents/router_agent.py`
- Execution agents: `backend/app/agents/*_agent.py`
- Audit agents: `backend/app/agents/*validator*.py`, `approval_gatekeeper.py`
- Memory: `backend/app/memory_engine.py`, `backend/app/agents/memory_agent.py`

## Advanced subagents
- Dynamic task graph + child tasks: `backend/app/task_queue.py`, `backend/app/agents/planner_agent.py`
- Subagent templates: `backend/app/agents/subagent_registry.py`

## Learning system
- Watch-to-Learn: `backend/app/learning/watch_to_learn.py`, `desktop_worker/workflow_watch.py`
- Search-to-Skill: `backend/app/learning/search_to_skill.py`
- Pattern detection: `backend/app/learning/pattern_detector.py`
- Suggest automations: `backend/app/learning/automation_suggester.py`
- Self-improving loop: `backend/app/learning/self_improver.py`
- Unified learning graph: `backend/app/learning_graph.py`

## Mobile app
- Dashboard/approvals/agents/preview/settings/knowledge/memory/skills/device control: `claw-agent/lib/screens/*`
- Voice/chat: `claw-agent/lib/core/voice_service.dart`
- Mobile-only spoken responses policy: `backend/app/voice_policy.py`, `claw-agent/lib/core/config.dart`

## Desktop + PC
- Desktop worker: `desktop_worker/worker.py`
- Windows silent PC agent: `pc_agent/claw_pc_agent.py`
- Remote wake/control: `backend/app/device_control.py`, `backend/app/wake_relay.py`, `backend/app/integrations/smart_plug.py`, `backend/app/integrations/amt_client.py`

## WhatsApp
- Extension inbound/outbound approval path: `extension/*`, `desktop_worker/whatsapp_bridge.py`, `backend/app/agents/whatsapp_agent.py`

## Offline/online + providers
- Provider switching: `backend/app/provider_router.py`
- Modes (fast/balanced/privacy): `backend/app/config.py`, `claw-agent/lib/core/config.dart`

## Integrations
- Google Sheets/Mail/Calendar: `backend/app/integrations/google_*`
- Supabase device/command sync: `backend/app/integrations/supabase_client.py`, `claw-agent/lib/core/supabase_service.dart`
