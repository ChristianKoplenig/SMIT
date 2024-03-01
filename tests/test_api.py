import pytest
from fastapi.testclient import TestClient

@pytest.mark.smoke
@pytest.mark.api
def test_api_healthchecker(test_app: TestClient) -> None:
    response = test_app.get("/api/healthchecker")
    assert response.status_code == 200
    assert {"message": "The API is LIVE!!"} == response.json()


#@pytest.mark.smoke
# @pytest.mark.api
# def test_database_connection(db_instance_empty: TestSmitDb,
#                              valid_users: dict[str, dict[str, str]],
#                              test_session: Session,
#                              test_app: TestClient) -> None:
    
#     # for user in valid_users.values():
#     #     instance: SQLModel = db_instance_empty.db_schema.model_validate(user)
#     #     db_instance_empty.create_instance(instance, session=test_session)
    
    
