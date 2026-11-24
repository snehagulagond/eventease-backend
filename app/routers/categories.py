from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import CategoryCreate,CategoryResponse
from ..models import Category,User
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
        name=category.name,
        description=category.description
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):

    categories = db.query(Category).all()

    return categories

@router.put("/{category_id}",response_model=CategoryResponse,status_code=status.HTTP_200_OK)
def update_category(category_id:int,category:CategoryCreate,current_user:User=Depends(require_role("admin")), db:Session=Depends(get_db)):
    existing_category=db.query(Category).filter(Category.id==category_id).first()
    if not existing_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")

    duplicate_category=db.query(Category).filter(Category.name==category.name,Category.id!=category_id).first()
    if duplicate_category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Category already exist")
    existing_category.name=category.name
    existing_category.description=category.description
    db.commit()
    db.refresh(existing_category)
    return existing_category

@router.delete("/{category_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id:int,current_user:User=Depends(require_role("admin")),db:Session=Depends(get_db)):
    existing_category=db.query(Category).filter(Category.id == category_id).first()
    if not existing_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")
    db.delete(existing_category)
    db.commit()

