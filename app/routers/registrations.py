from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..database import get_db
from .auth import get_current_user
from ..models import User,Event,Registration

router=APIRouter(
    prefix="/registrations",
    tags=["registrations"]
)
@router.post("/{event_id}",status_code=status.HTTP_201_CREATED)
def register_for_event(event_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    event=db.query(Event).filter(Event.id==event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Event not found")
    registration=db.query(Registration).filter(Registration.event_id==event_id,Registration.user_id==current_user.id).first()
    if registration:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="You have already registered for this event")
    event_capacity=db.query(Registration).filter(Registration.event_id==event_id).count()
    if event_capacity>=event.capacity:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Event is full")
    new_registration=Registration(
        event_id=event_id,
        user_id=current_user.id
    )
    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)
    return {"message":"Successfully registered for the event"}

@router.get("/my",status_code=status.HTTP_200_OK)
def get_user_registrations(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    registrations=db.query(Registration).filter(Registration.user_id==current_user.id).all()
    return registrations

@router.delete("/{event_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_registration(event_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    registration=db.query(Registration).filter(Registration.event_id==event_id,Registration.user_id==current_user.id).first()
    if not registration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Registration not found")

    db.delete(registration)
    db.commit()


