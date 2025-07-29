from app.managers.person import PersonManager
from app.models.person import PersonIn, PersonUpdate

def test_create_and_get_person(db):
    manager = PersonManager(db)
    data = PersonIn(name="Alice", age=30, city="Kyiv")
    person = manager.create(data)

    assert person.id is not None, "person not created"
    assert person.name == "Alice", f"person name not corrrect. expected: Alice actual: {person.name}"

    loaded = manager.get(person.id)
    assert loaded.name == "Alice"
    assert loaded.age == 30
    assert loaded.city == "Kyiv"

def test_update_person(db):
    manager = PersonManager(db)
    person = manager.create(PersonIn(name="Bob", age=25, city="Lviv"))

    updated = manager.update(person.id, PersonUpdate(age=26))
    assert updated.age == 26
    assert updated.name == "Bob"  # інші поля не змінюються
    assert updated.city == "Lviv"

def test_delete_person(db):
    manager = PersonManager(db)
    person = manager.create(PersonIn(name="Charlie", age=40, city="Odessa"))

    ok = manager.delete(person.id)
    assert ok is True

    deleted = manager.get(person.id)
    assert deleted is None

def test_list_all(db):
    manager = PersonManager(db)
    manager.create(PersonIn(name="X", age=20, city="A"))
    manager.create(PersonIn(name="Y", age=21, city="B"))

    people = manager.list_all()
    assert len(people) == 2
