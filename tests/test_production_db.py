import pytest
from fastapi.testclient import TestClient
from httpx import Response
from api.main import app

from utils import users_mock

client = TestClient(app)


@pytest.mark.smoke
@pytest.mark.production
def test_production_api_healthchecker() -> None:
    """Use testclient for health check."""
    response: Response = client.get("/api/healthchecker")
    assert response.status_code == 200
    assert {"message": "The API is LIVE!!"} == response.json()


# @pytest.mark.smoke
# @pytest.mark.production
# def test_production_post_user() -> None:
#     """Access production database."""
#     user: dict[str, str] = users_mock.valid_users()[0]

#     response: Response = client.post("/users/user/create", json=user)

#     assert response.status_code == 400