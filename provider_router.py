from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class ProviderDecision:
    provider: str
    mode: str
    online: bool
    reason: str
    fallback_chain: list[str]


class ProviderRouter:
    ONLINE_HINTS = {'gmail', 'email', 'calendar', 'sheet', 'sheets', 'search', 'web', 'whatsapp', 'browser', 'supabase'}
    LOCAL_HINTS = {'privacy', 'offline', 'local', 'draft', 'learn', 'pattern', 'memory', 'skill'}

    def classify(self, task_title: str, action_type: str = '', payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = payload or {}
        text = f"{task_title or ''} {action_type or ''} {payload}".lower()
        requires_online = any(k in text for k in self.ONLINE_HINTS)
        privacy_preferred = any(k in text for k in self.LOCAL_HINTS)
        heavy_reasoning = any(k in text for k in ['plan', 'analyze', 'reason', 'subagent', 'complex'])
        return {
            'requires_online': requires_online,
            'privacy_preferred': privacy_preferred,
            'heavy_reasoning': heavy_reasoning,
        }

    def decide(self, task_title: str, mode: str = 'balanced', requires_online: bool = False, action_type: str = '', payload: dict[str, Any] | None = None) -> ProviderDecision:
        signals = self.classify(task_title, action_type, payload)
        online = requires_online or signals['requires_online']
        if mode == 'privacy' and not online:
            return ProviderDecision('local', 'privacy', False, 'Privacy mode keeps task offline.', ['anthropic', 'openai'])
        if online:
            primary = 'gemini' if 'search' in (task_title or '').lower() or action_type == 'web_search' else 'openai'
            return ProviderDecision(primary, mode, True, 'Task needs live integrations or internet.', ['anthropic', 'gemini', 'local'])
        if mode == 'fast':
            return ProviderDecision('local', 'fast', False, 'Fast mode prefers local execution.', ['openai', 'anthropic'])
        if signals['heavy_reasoning']:
            return ProviderDecision('anthropic', mode, False, 'Balanced mode selected heavier reasoning provider.', ['openai', 'local'])
        return ProviderDecision('local', mode, False, 'Balanced mode selected offline-first local provider.', ['anthropic', 'openai'])
