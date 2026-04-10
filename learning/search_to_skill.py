from __future__ import annotations
from sqlalchemy.orm import Session
from ..models import LearningEvent, KnowledgeItem, Preview
from ..skills_engine import create_skill


def convert_search_to_skill(db: Session, query: str, learned_summary: str, project_key: str = "default"):
    db.add(LearningEvent(source="search", event_type="query", payload=query, confidence=70, project_key=project_key))
    db.add(KnowledgeItem(project_key=project_key, title=f"Search knowledge: {query[:80]}", body=learned_summary or query))
    db.commit()
    skill = create_skill(db, name=f"Skill from search: {query[:40]}", logic=learned_summary or query, source="search_to_skill")
    db.add(Preview(preview_type='skill', left_content=query, right_content=learned_summary or query))
    db.commit()
    return skill
