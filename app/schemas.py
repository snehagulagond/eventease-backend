from pydantic import BaseModel,ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    name:str
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    name:str
    email:str
    role:str
    model_config=ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str


class EventCreate(BaseModel):
    title:str
    description:str
    date:datetime
    location:str
    capacity:int
    
class EventResponse(BaseModel):
    id:int
    organizer_id:int
    title:str
    description:str
    date:datetime
    location:str
    capacity:int
    model_config=ConfigDict(from_attributes=True) #so that pydantic can read from ORM models(SQLAlchemy model objects) and convert them to Pydantic models. This is useful when you want to return data from your database as a response in your API endpoints.
