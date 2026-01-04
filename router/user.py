

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dependency import get_db
from models.user_models import User
from schemas.users_schemas import UserCreate , UserLogin,UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# 🔹 Get all users
@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# 🔹 Get user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 🔹 Get user by name
@router.get("/by-name/{username}", response_model=List[UserResponse])
def get_user_by_name(username: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.username.ilike(f"%{username}%")).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# 🔹 Signup
@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password  # later hash it
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 🔹 Login
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.email == user.email,
        User.password == user.password
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "username": db_user.username
    }
