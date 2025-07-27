from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse

from app.database import get_db
from app.models.person import PersonIn, PersonOut, PersonUpdate
from app.managers.person import PersonManager

router = APIRouter(tags=["HTML"])
templates = Jinja2Templates(directory="app/templates")
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request, db: Session = Depends(get_db)):
    people = PersonManager(db).list_all()
    return templates.TemplateResponse("show_people_list.html", {
        "request": request,
        "people": people
    })

@router.get("/add", response_class=HTMLResponse
    , summary="add person form"
    , description="show form for add person")
def show_add_form(request: Request):
    return templates.TemplateResponse("add_person_form.html", {"request": request})

@router.post("/add")
def handle_form(
    name: str = Form(...),
    age: int = Form(...),
    city: str = Form(...),
    db: Session = Depends(get_db)
):
    person = PersonIn(name=name, age=age, city=city)
    person = PersonManager(db).create(person)
    db.add(person)
    db.commit()
    return RedirectResponse(url="/", status_code=303)
