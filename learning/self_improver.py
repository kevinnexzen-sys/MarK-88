def self_improve_snapshot(approvals: int, rejections: int, successful_skills: int):
    score = max(0, min(100, 50 + approvals * 2 - rejections * 2 + successful_skills * 3))
    return {"improvement_score": score, "approvals": approvals, "rejections": rejections, "successful_skills": successful_skills}
