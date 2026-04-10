from sqlalchemy.orm import Session
from .models import MemoryEntry

def remember(db: Session, title: str, content: str, entry_type: str = "general", project_key: str = "default", tags: str = ""):
    entry = MemoryEntry(title=title, content=content, entry_type=entry_type, project_key=project_key, tags=tags)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def search_memory(db: Session, query: str):
    q = f"%{query.lower()}%"
    return db.query(MemoryEntry).filter(MemoryEntry.content.ilike(q) | MemoryEntry.title.ilike(q)).all()
