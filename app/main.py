from fastapi import FastAPI
from .database import Base,engine,SessionLocal
from .import models

app=FastAPI()
Base.metadata.create_all(bind=engine)
@app.get("/")
def read_root():
    return {"Project":"Welcome users to EventEase"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/about")
def about():
    return {
  "project": "EventEase",
  "description": "Event Management and Registration API",
  "version": "1.0",
  "purpose": "A platform to discover and register for events"
}

@app.get("/categories")
def read_categories():
    return {
  "categories": [
    "Technical",
    "Cultural",
    "Sports",
    "Workshop",
    "Conference",
    "Hackathon"
  ]
}

@app.get("/welcome")
def read_welcome():
    return {"message": "Welcome to EventEase! Explore and register for exciting events."}
