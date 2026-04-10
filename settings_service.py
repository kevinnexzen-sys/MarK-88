from sqlalchemy.orm import Session
from .models import Setting


def get_all_settings(db: Session):
    rows = db.query(Setting).all()
    grouped = {}
    for row in rows:
        grouped.setdefault(row.group_name, {})[row.key] = row.value
    return grouped


def get_group_settings(db: Session, group_name: str):
    rows = db.query(Setting).filter(Setting.group_name == group_name).all()
    return {row.key: row.value for row in rows}


def get_setting(db: Session, group_name: str, key: str, default: str = "") -> str:
    row = db.query(Setting).filter(Setting.group_name == group_name, Setting.key == key).first()
    return row.value if row else default


def put_settings(db: Session, items):
    for item in items:
        row = db.query(Setting).filter(Setting.group_name == item.group_name, Setting.key == item.key).first()
        if row:
            row.value = item.value
        else:
            db.add(Setting(group_name=item.group_name, key=item.key, value=item.value))
    db.commit()
    return get_all_settings(db)
