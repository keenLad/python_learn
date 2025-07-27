from sqlalchemy.orm import Session
from app.models.person import Person, PersonIn, PersonUpdate

class PersonManager:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self):
        return self.db.query(Person).all()

    def get(self, person_id: int):
        return self.db.query(Person).get(person_id)

    def create(self, data: PersonIn):
        person = Person(**data.dict())
        self.db.add(person)
        self.db.commit()
        self.db.refresh(person)
        return person

    def update(self, person_id: int, data: PersonUpdate):
        person = self.get(person_id)
        if not person:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(person, key, value)
        self.db.commit()
        self.db.refresh(person)
        return person

    def delete(self, person_id: int):
        person = self.get(person_id)
        if not person:
            return False
        self.db.delete(person)
        self.db.commit()
        return True