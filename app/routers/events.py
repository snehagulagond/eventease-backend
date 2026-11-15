from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import EventCreate,EventResponse
from ..models import Event,User
from .auth import get_current_user
from typing import List

router=APIRouter(
    prefix="/events",
    tags=["events"]

)
@router.post("/",response_model=EventResponse,status_code=status.HTTP_201_CREATED)
def create_event(event:EventCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    #Create a new event instance
    new_event=Event(
        organizer_id=current_user.id,
        title=event.title,
        description=event.description,
        date=event.date,
        location=event.location,
        capacity=event.capacity

    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/",response_model=List[EventResponse],status_code=status.HTTP_200_OK)
def get_all_events(db:Session=Depends(get_db)):
    events=db.query(Event).all()
    return events

@router.get("/{event_id}",response_model=EventResponse,status_code=status.HTTP_200_OK)
def get_event(event_id:int,db:Session=Depends(get_db)):
    event=db.query(Event).filter(Event.id==event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Event not found")
    return event

@router.put("/{event_id}",response_model=EventResponse,status_code=status.HTTP_200_OK)
def update_event(event_id:int,event:EventCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    existing_event=db.query(Event).filter(Event.id==event_id).first()
    if not existing_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Event not found")
    if existing_event.organizer_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not the organizer of this event")

        existing_event.title=event.title
        existing_event.description=event.description
        existing_event.date=event.date
        existing_event.Location=event.location
        existing_event.capacity=event.capacity
        db.commit()
        db.refresh(existing_event)
        return existing_event
            
@router.delete("/{event_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    existing_event=db.query(Event).filter(Event.id==event_id).first()
    if not existing_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Event not found")
    if existing_event.organizer_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not the organizer of this event")
    db.delete(existing_event)
    db.commit()

