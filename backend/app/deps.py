from fastapi import Depends, HTTPException, status
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app import auth as auth_utils
from app import crud, models
from app.schemas import TokenData
from typing import Generator

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth_utils.verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user_id = payload.get("user_id")
    role = payload.get("role")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def require_roles(*allowed_roles):
    def role_checker(user: models.User = Depends(get_current_user)):
        if user.role.value not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")
        return user
    return role_checker
