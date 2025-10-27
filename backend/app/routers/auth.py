from fastapi import APIRouter, Depends, HTTPException, status
from app import crud
from app.schemas import UserCreate, Token
from app.auth import create_access_token
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.deps import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db, user_in.name, user_in.email, user_in.password, user_in.role.value)
    token = create_access_token({"user_id": user.id, "role": user.role.value})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = create_access_token({"user_id": user.id, "role": user.role.value})
    return {"access_token": token, "token_type": "bearer"}

# 🧪 Test route to verify frontend-backend connection
@router.get("/test")
def test_connection():
    return {"message": "✅ Backend connected successfully!"}
