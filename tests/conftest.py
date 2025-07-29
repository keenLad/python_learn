import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.person import Base

# Тестовий engine у пам'яті
SQLALCHEMY_TEST_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db():
    engine = create_engine(SQLALCHEMY_TEST_URL)
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
