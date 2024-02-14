from typing import Any, Generator
import pytest
from fastapi.testclient import TestClient

from api.main import app
from db.connection import get_db

# For type hinting
from sqlmodel import Session, SQLModel
from .conftest import TestSmitDb

@pytest.mark.smoke
#@pytest.mark.api
def test_root(test_app: TestClient) -> None:
    response = test_app.get("/api/healthchecker")
    assert response.status_code == 200
    assert response.json() == {"message": "The API is LIVE!!"}

@pytest.mark.smoke
@pytest.mark.api
def test_database_connection(db_instance_empty: TestSmitDb,
                             valid_users: dict[str, dict[str, str]],
                             test_session: Session,
                             test_app: TestClient) -> None:
    
    for user in valid_users.values():
        instance: SQLModel = db_instance_empty.db_schema.model_validate(user)
        db_instance_empty.create_instance(instance, session=test_session)
    
    response = test_app.get("/auth/users")
    assert response.status_code == 200
    assert {"username": "dummy_user"} in response.json()
