from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models import models
from schemas.auth import UserCreate, UserLogin, SignUpRespone, LoginResponse
from utils.security import get_password, verify_password
from utils.jwt import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["auth", "signup", "login"])

@router.post("/signup", response_model=SignUpRespone, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    
    existing_user = db.query(models.User).filter(user.email == models.User.email).first()

    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "User already exist with provided email"
        )
    
    hashed_password = get_password(user.password)
    
    new_user = models.User(
        full_name = user.full_name,
        email = user.email,
        hashed_password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "data": new_user
    }

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(user: UserLogin, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid credentials"
        )
    
    access_token = create_access_token(
        data = {"sub": str(existing_user.id)}
    )

    refresh_token = create_refresh_token(
        data = {"sub": str(existing_user.id)}
    )

    existing_user.hashed_refresh_token = get_password(refresh_token)
    db.commit()
    
    return {
        "message": "User logged in successfully",
        "data": existing_user,
        "token": {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    }