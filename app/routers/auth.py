from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserCreate,UserResponse,UserLogin,Token
from ..models import User
from ..security import hash_password,verify_password,create_access_token,oauth2_scheme,SECRET_KEY,ALGORITHM
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordRequestForm




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

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login_user(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # Check if the user exists
    existing_user = db.query(User).filter(User.email == user.username).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify the password
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT access token
    access_token = create_access_token(
        data={"sub": str(existing_user.id)}
    )

    # Return token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    # Fetch the user from the database
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
