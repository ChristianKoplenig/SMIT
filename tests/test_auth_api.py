import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from .conftest import TestSmitDb
from api.schemas import UserResponseSchema


@pytest.mark.smoke
@pytest.mark.authentication
def test_auth_get_user(
    test_app: TestClient,
    api_test_session: Session,
    api_instance_empty: TestSmitDb,
    valid_users: dict[str, dict[str, str]],
    ) -> None:
    """Test authentication get_user endpoint."""

    ### Use TestSmitDb ###
    # Validate input for creating user entry in database
    instance = api_instance_empty.db_schema.model_validate(valid_users['dummy_user'])
    # Use SmitDb from crud.py to create user entry in database
    api_instance_empty.create_instance(instance, session=api_test_session)
    assert instance.username == 'dummy_user'

    ### Use API test client ###
    # Test get_user endpoint
    response = test_app.get('/auth/user/dummy_user')
    assert response.status_code == 200
    assert 'dummy_user' in response.json().values()

    # Assert response schema
    user = UserResponseSchema(**response.json())
    for each in valid_users['dummy_user']:
        assert getattr(user, each) == valid_users['dummy_user'][each]