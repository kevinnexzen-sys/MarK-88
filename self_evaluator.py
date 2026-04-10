import json

def evaluate_task_output(task_title: str, draft_output: str) -> dict:
    issues = []
    confidence = 85
    if not draft_output.strip():
        issues.append("Draft output is empty")
        confidence -= 45
    if len(draft_output.strip()) < 40:
        issues.append("Draft output is very short")
        confidence -= 10
    if "TODO" in draft_output or "placeholder" in draft_output.lower():
        issues.append("Contains placeholder content")
        confidence -= 15
    if any(k in task_title.lower() for k in ["send", "reply", "email", "whatsapp", "sheet", "calendar"]):
        confidence = min(confidence, 80)
    status = "ready_for_review" if confidence >= 70 else "needs_review"
    return {"confidence": max(0, min(100, confidence)), "issues": issues, "status": status}

def dumps_eval(data: dict) -> str:
    return json.dumps(data)
