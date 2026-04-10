from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Role
from ..schemas import LoginRequest, LoginResponse, UserOut, ChangePasswordRequest
from ..auth import verify_password, create_session_token, get_current_user, hash_password

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    role = db.query(Role).filter(Role.id == user.role_id).first()
    token = create_session_token(user, db)
    return LoginResponse(token=token, user=UserOut(username=user.username, role=role.name if role else "unknown"))

@router.get("/me")
def me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == user.role_id).first()
    return {"username": user.username, "role": role.name if role else "unknown"}

@router.post("/logout")
def logout(user: User = Depends(get_current_user)):
    return {"status": "ok"}

@router.post("/change-password")
def change_password(payload: ChangePasswordRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Current password incorrect")
    user.password_hash = hash_password(payload.new_password)
    db.commit()
    return {"status": "ok"}
