from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    role=Column(String,nullable=False,server_default='user')
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Event(Base):
    __tablename__="events"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    description=Column(String,nullable=False)
    date=Column(DateTime,nullable=False)
    location=Column(String,nullable=False)
    capacity=Column(Integer,nullable=False)
    organizer_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

class Registration(Base):
    __tablename__="registrations"
    id=Column(Integer,primary_key=True,nullable=False)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    event_id=Column(Integer,ForeignKey("events.id",ondelete="CASCADE"),nullable=False)
    status=Column(String,nullable=False,server_default='registered')

class Category(Base):
    __tablename__="categories"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False,unique=True)
    