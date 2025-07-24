from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Person(BaseModel):
    name: str
    age: int
    city: str

people: List[Person] = []

@app.get("/")
def home():
    return {"message": "Привіт з FastAPI!"}

@app.post("/people")
def add_person(person: Person):
    people.append(person)
    return {"added": person}

@app.get("/people")
def list_people():
    return people
