from __future__ import annotations

SUBAGENT_TEMPLATES = {
    'estimate': ['EstimateAgent', 'SOPValidator', 'PricingValidator', 'ContaminationChecker'],
    'integration': ['SheetsAgent', 'EmailAgent', 'CalendarAgent'],
    'communications': ['WhatsAppAgent', 'EmailAgent'],
    'codegen': ['CodegenAgent', 'ApprovalGatekeeper'],
    'learning': ['WatchToLearnAgent', 'SearchToSkillAgent', 'PatternDetectionAgent', 'AutomationSuggestionAgent'],
}


def choose_templates(task_title: str) -> list[str]:
    t = (task_title or '').lower()
    if 'estimate' in t:
        return SUBAGENT_TEMPLATES['estimate']
    if any(k in t for k in ['sheet', 'email', 'calendar', 'work order']):
        return SUBAGENT_TEMPLATES['integration']
    if any(k in t for k in ['whatsapp', 'chat', 'reply']):
        return SUBAGENT_TEMPLATES['communications']
    if any(k in t for k in ['code', 'app', 'preview']):
        return SUBAGENT_TEMPLATES['codegen']
    return ['RouterAgent', 'ApprovalGatekeeper']
