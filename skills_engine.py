from sqlalchemy.orm import Session
from .models import Skill

def create_skill(db: Session, name: str, logic: str, source: str = "generated"):
    skill = Skill(name=name, logic=logic, source=source, status="draft")
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill
