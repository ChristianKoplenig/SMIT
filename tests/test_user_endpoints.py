import pytest
from fastapi.testclient import TestClient
from httpx import Response

from utils import users_mock

@pytest.mark.smoke
@pytest.mark.api
def test_testclient(api_testclient: TestClient) -> None:
    """Test fastapi mocked testclient connection."""
    health: Response = api_testclient.get("/api/healthchecker")
    assert health.status_code == 200


@pytest.mark.smoke
@pytest.mark.api
def test_post_user(api_testclient: TestClient) -> None:
    """Use mocked testclient to post user on testing database."""
    user: dict[str, str] = users_mock.valid_users()[0]

    response: Response = api_testclient.post("/crud/user/create", json=user)

    assert response.status_code == 200