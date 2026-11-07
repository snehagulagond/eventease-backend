from fastapi import APIRouter,Depends, HTTPException, status
from app.routers.auth import router
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserCreate,UserResponse
from ..models import User
from ..security import hash_password,verify_password

router=APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)

def register_user(user:UserCreate, db:Session=Depends(get_db)):
    # Check if the email already exists
    existing_user=db.query(User).filter(User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
    # Hash the password
    hashed_password=hash_password(user.password)
    
    # Create a new user instance
    new_user=User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )
    
    # Add and commit the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user