from sqlalchemy.orm import Session
from ..memory_engine import remember, search_memory

class MemoryAgent:
    def store(self, db: Session, title: str, content: str, entry_type: str = "general", project_key: str = "default"):
        return remember(db, title=title, content=content, entry_type=entry_type, project_key=project_key)

    def search(self, db: Session, query: str):
        return search_memory(db, query)
