from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database.base import Base
from app.dependencies.database import get_db
from app.main import app
from app.models.book import Book
from app.models.user import User
import pytest
from fastapi.testclient import TestClient


TEST_DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}"
    f"/{settings.TEST_DB_NAME}"
)


test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client