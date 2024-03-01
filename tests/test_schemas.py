
import pytest
from typing import TYPE_CHECKING
from sqlmodel import Session

from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from tests.conftest import TestSmitDb

from schemas.user_schemas import UserBase

if TYPE_CHECKING:
    from sqlmodel import SQLModel

### Needed for warning output
# Used to validate if all field constraints are met
import warnings
###

# Test database model
@pytest.mark.smoke
@pytest.mark.schemas
def test_invalid_users(
    invalid_users: dict[str, dict[str, str]],
    db_instance_empty: TestSmitDb
) -> None:
    for user in invalid_users:
        with pytest.raises(ValueError):
            db_instance_empty.db_schema.model_validate(invalid_users[user])

@pytest.mark.smoke
@pytest.mark.schemas
def test_valid_users(
    valid_users: dict[str, dict[str, str]],
    db_instance_empty: TestSmitDb
) -> None:
    for user in valid_users:
        db_instance_empty.db_schema.model_validate(valid_users[user])

@pytest.mark.smoke
@pytest.mark.schemas
def test_unique_constraint(
    valid_users: dict[str, dict[str, str]],
    db_instance_empty: TestSmitDb,
    test_session: Session,
) -> None:
    user1: SQLModel = db_instance_empty.db_schema.model_validate(valid_users["dummy_user"])
    user2: SQLModel = db_instance_empty.db_schema.model_validate(valid_users["dummy_user"])

    with test_session:
        with pytest.raises(IntegrityError):
            test_session.add(user1)
            test_session.add(user2)
            test_session.commit()

# Test Api schemas
@pytest.mark.smoke
@pytest.mark.schemas
def test_api_userbase_schema(
    invalid_users: dict[str, dict[str, str]],
    valid_users: dict[str, dict[str, str]],
) -> None:
    """Validate the UserBase schema.

    Test valid users and exceptions for invalid users.
    Additionally, show warnings for validating field constraints output.

    Args:
        invalid_users (dict[str, dict[str, str]]): A dictionary of invalid user data.
        valid_users (dict[str, dict[str, str]]): A dictionary of valid user data.

    Returns:
        None
    """
    # Test valid users
    for user in valid_users:
        UserBase.model_validate(valid_users[user])

    # Test exceptions for invalid users
    with pytest.raises(ValidationError):
        for user in invalid_users:
            UserBase.model_validate(invalid_users[user])

    # Show warnings to validate each field constraint output
    # for user in invalid_users:
    #     try:
    #         schemas.UserBase.model_validate(invalid_users[user])
    #     except ValidationError as ve:
    #         warnings.warn(str(AuthValidateError(ve)), UserWarning)

@pytest.mark.smoke
@pytest.mark.schemas
def test_api_unique_constraint(
    valid_users: dict[str, dict[str, str]],
    api_instance_empty: TestSmitDb,
    api_test_session: Session,
) -> None:
    user1: SQLModel = api_instance_empty.db_schema.model_validate(
        valid_users["dummy_user"]
    )
    user2: SQLModel = api_instance_empty.db_schema.model_validate(
        valid_users["dummy_user"]
    )

    with api_test_session:
        with pytest.raises(IntegrityError):
            api_test_session.add(user1)
            api_test_session.add(user2)
            api_test_session.commit()