from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import CategoryCreate,CategoryResponse
from ..models import Category
from .auth import require_role

router=APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.post("/",response_model=CategoryResponse,status_code=status.HTTP_201_CREATED)
def create_category(category:CategoryCreate,current_user:User=Depends(require_role("admin")), db:Session=Depends(get_db)):
    existing_category=db.query(Category).filter(Category.name==category.name).first()
    if  existing_category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Category already exists")
    new_category=Category(
        name=category.name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):

    categories = db.query(Category).all()

    return categories