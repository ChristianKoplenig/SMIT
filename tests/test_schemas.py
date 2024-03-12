
import pytest
from typing import List
from typing import TYPE_CHECKING
from sqlmodel import Session, SQLModel

from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from utils import users_mock
from utils.logger import Logger
from database.db_models import UserModel


### Needed for warning output
# Used to validate if all field constraints are met
import warnings
###

# Test database models
@pytest.mark.smoke
@pytest.mark.schemas
def test_invalid_users() -> None:
    """Test UserModel validation."""
    
    invalid_users: List[dict[str, str]] = users_mock.invalid_users()

    for user in invalid_users:
        with pytest.raises(ValidationError):
            Logger().logger.debug(f"Testing invalid user: {user['username']}")
            UserModel.model_validate(user)

@pytest.mark.smoke
@pytest.mark.schemas
def test_valid_users() -> None:
    """Test UserModel validation."""

    valid_users: List[dict[str, str]] = users_mock.valid_users()

    for user in valid_users:
        Logger().logger.debug(f"Testing valid user: {user['username']}")
        UserModel.model_validate(user)