from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.person import PersonIn, PersonOut, PersonUpdate
from app.managers.person import PersonManager

router = APIRouter(tags=["API"])

@router.get("/people", response_model=list[PersonOut])
def list_people(db: Session = Depends(get_db)):
    return PersonManager(db).list_all()

@router.get("/people/{person_id}", response_model=PersonOut)
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = PersonManager(db).get(person_id)
    if not person:
        raise HTTPException(404, detail="Not found")
    return person

@router.post("/people", response_model=PersonOut)
def add_person(data: PersonIn, db: Session = Depends(get_db)):
    return PersonManager(db).create(data)

@router.put("/people/{person_id}", response_model=PersonOut)
def update_person(person_id: int, data: PersonUpdate, db: Session = Depends(get_db)):
    updated = PersonManager(db).update(person_id, data)
    if not updated:
        raise HTTPException(404, detail="Not found")
    return updated

@router.delete("/people/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    ok = PersonManager(db).delete(person_id)
    if not ok:
        raise HTTPException(404, detail="Not found")
    return {"deleted_id": person_id}