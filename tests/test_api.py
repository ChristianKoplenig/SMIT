import pytest
from fastapi.testclient import TestClient
from httpx import Response

from utils import users_mock

from exceptions.db_exc import DatabaseError

@pytest.mark.smoke
#@pytest.mark.api
def test_testclient(api_testclient: TestClient) -> None:
    """Test fastapi mocked testclient connection."""
    health: Response = api_testclient.get("/api/healthchecker")
    assert health.status_code == 200

@pytest.mark.smoke
#@pytest.mark.api
def test_post_user(api_testclient: TestClient) -> None:
    """Use mocked testclient to post user on testing database."""
    user_dict: dict[str, str] = users_mock.valid_users()[0]

    response: Response = api_testclient.post("/users/user/create", json=user_dict)

    assert response.status_code == 200

@pytest.mark.smoke
#@pytest.mark.api
def test_post_invalid_user(api_testclient: TestClient) -> None:
    """Use mocked testclient to post user on testing database."""
    user_dict: dict[str, str] = users_mock.invalid_users()[0]

    response: Response = api_testclient.post("/users/user/create", json=user_dict)

    assert response.status_code == 422

@pytest.mark.smoke
#@pytest.mark.api
def test_get_user(api_testclient: TestClient) -> None:
    """Use mocked testclient to get user from testing database."""
    user_dict: dict[str, str] = users_mock.valid_users()[0]

    api_testclient.post("/users/user/create", json=user_dict)

    response: Response = api_testclient.get("/users/user/dummy_user")

    assert response.status_code == 200
    assert response.json()["username"] == "dummy_user"

    assert False

@pytest.mark.smoke
#@pytest.mark.api
def test_get_nonexisting_user(api_testclient: TestClient) -> None:
    """Use mocked testclient to get user from testing database."""
    user_dict: dict[str, str] = users_mock.valid_users()[0]

    api_testclient.post("/users/user/create", json=user_dict)

    response404: Response = api_testclient.get("/users/user/wrong_user")
    assert response404.status_code == 404

@pytest.mark.smoke
@pytest.mark.api
def test_get_all_users(api_testclient: TestClient) -> None:
    """Use mocked testclient to get all users from testing database."""

    for each in users_mock.valid_users():
        api_testclient.post("/users/user/create", json=each)

    response: Response = api_testclient.get("/users/allusers")

    assert response.status_code == 200
    assert len(response.json()['userlist']) == len(users_mock.valid_users())
    assert 'dummy_user' in response.json()['userlist']