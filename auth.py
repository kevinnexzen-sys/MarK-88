import base64
import secrets
from fastapi import Depends, Header, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .database import get_db
from .models import User, Role

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_session_token(user: User, db: Session) -> str:
    role = db.query(Role).filter(Role.id == user.role_id).first()
    payload = f"{user.username}:{role.name if role else 'unknown'}:{secrets.token_urlsafe(8)}"
    return base64.urlsafe_b64encode(payload.encode()).decode()

def get_current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split(" ", 1)[1]
    try:
        decoded = base64.urlsafe_b64decode(token.encode()).decode()
        username = decoded.split(':', 1)[0]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid session")
    user = db.query(User).filter(User.username == username, User.active == True).first()  # noqa: E712
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_role(allowed: list[str]):
    def _dep(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        role = db.query(Role).filter(Role.id == user.role_id).first()
        if not role or role.name not in allowed:
            raise HTTPException(status_code=403, detail="Insufficient role")
        return user
    return _dep
