from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import traceback
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, Role
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from app.services.auth import (
    get_password_hash,
    create_access_token,
    verify_password,
    get_current_user
)

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    role = db.query(Role).filter(Role.id == user.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")

    db_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
        role_id=user.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.email == form_data.username).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Wrong password")

        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        # 🔴 ПЕЧАТАЕМ ОШИБКУ В КОНСОЛЬ UVICORN
        print("\n🚨 ОШИБКА В LOGIN:")
        print(traceback.format_exc())
        # 🔴 ВОЗВРАЩАЕМ ТЕКСТ ОШИБКИ В SWAGGER
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user