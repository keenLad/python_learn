from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from database import SessionLocal, engine
from models import Base, Person as PersonModel

class Utf8JSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

app = FastAPI(default_response_class=Utf8JSONResponse)

Base.metadata.create_all(bind=engine)

class PersonIn(BaseModel):
    name: str
    age: int
    city: str

class PersonOut(PersonIn):
    id: int

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Привіт з FastAPI та PostgreSQL!"}

@app.post("/people", response_model=PersonOut)
def add_person(person: PersonIn, db: Session = Depends(get_db)):
    db_person = PersonModel(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@app.get("/people", response_model=List[PersonOut])
def list_people(db: Session = Depends(get_db)):
    return db.query(PersonModel).all()