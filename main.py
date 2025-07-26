from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


from database import SessionLocal, engine
from models import Base, Person as PersonModel

class Utf8JSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

app = FastAPI(default_response_class=Utf8JSONResponse)
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

class PersonIn(BaseModel):
    name: str
    age: int
    city: str

class PersonOut(PersonIn):
    id: int

    class Config:
        orm_mode = True

class PersonUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    people = db.query(PersonModel).all()
    return templates.TemplateResponse("show_people_list.html", {
        "request": request,
        "people": people
    })

@app.get("/add", response_class=HTMLResponse)
def show_add_form(request: Request):
    return templates.TemplateResponse("add_person_form.html", {"request": request})

@app.post("/add")
def handle_form(
    name: str = Form(...),
    age: int = Form(...),
    city: str = Form(...),
    db: Session = Depends(get_db)
):
    person = PersonModel(name=name, age=age, city=city)
    db.add(person)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

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

@app.get("/people/{person_id}", response_model=PersonOut)
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(PersonModel).get(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@app.put("/people/{person_id}", response_model=PersonOut)
def update_person(person_id: int, updated: PersonUpdate, db: Session = Depends(get_db)):
    person = db.query(PersonModel).get(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(person, key, value)

    db.commit()
    db.refresh(person)
    return person

@app.delete("/people/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(PersonModel).get(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    db.delete(person)
    db.commit()
    return {"deleted_id": person_id}
