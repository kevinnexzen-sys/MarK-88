from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _ensure_sqlite_columns():
    insp = inspect(engine)
    if 'tasks' in insp.get_table_names():
        cols = {c['name'] for c in insp.get_columns('tasks')}
        statements = []
        if 'action_type' not in cols:
            statements.append("ALTER TABLE tasks ADD COLUMN action_type VARCHAR(80) DEFAULT ''")
        if 'action_payload_json' not in cols:
            statements.append("ALTER TABLE tasks ADD COLUMN action_payload_json TEXT DEFAULT '{}' ")
        if statements:
            with engine.begin() as conn:
                for stmt in statements:
                    conn.execute(text(stmt))


def init_db():
    from . import models  # noqa
    Base.metadata.create_all(bind=engine)
    _ensure_sqlite_columns()
