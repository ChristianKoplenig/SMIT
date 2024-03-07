"""Test database users_crud directly."""
import pytest
from typing import Annotated
from sqlmodel import Session

from database.db_users import Users
from database.db_models import UserModel
from utils import users_mock

from exceptions.db_exc import DatabaseError

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
async def test_create_user(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Test creating a user."""
    session: Session = empty_test_db
    user: dict[str, str] = users_mock.valid_users()[0]
    db_user: UserModel = UserModel.model_validate(user)
    on_db: UserModel = await Users().create_user(
        db_user,
        session=session)
    assert on_db.username == db_user.username
    assert on_db.email == db_user.email
    assert on_db.daymeter == db_user.daymeter


@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
async def test_create_user_exception(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Test for database error when username already exists."""
    session: Session = empty_test_db
    user: dict[str, str] = users_mock.valid_users()[0]
    user1: dict[str, str] = users_mock.valid_users()[0]
    db_user: UserModel = UserModel.model_validate(user)
    db_user1: UserModel = UserModel.model_validate(user1)

    with pytest.raises(DatabaseError) as dbe:
        on_db: UserModel = await Users().create_user(
            db_user,
            session= session)

        on_db1: UserModel = await Users().create_user(
            db_user1,
            session=session)
    assert "IntegrityError" in str(dbe.value)
        
    