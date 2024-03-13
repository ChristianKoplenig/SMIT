"""Test database users_crud directly."""
import pytest
from typing import Annotated
from sqlmodel import Session, SQLModel

from database.crud import Crud
from database.db_models import UserModel
from schemas.user_schemas import UserResponseSchema
from utils import users_mock
from utils.logger import Logger

from exceptions.db_exc import DatabaseError

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
async def test_post(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Use UserModel to test post method."""
    session: Session = empty_test_db
    user: dict[str, str] = users_mock.valid_users()[0]
    db_user: UserModel = UserModel.model_validate(user)
    on_db: SQLModel = await Crud().post(
        datamodel=db_user,
        session=session)
    assert on_db.username == db_user.username
    assert on_db.email == db_user.email
    assert on_db.daymeter == db_user.daymeter


@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
async def test_post_exception(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Test for database error when username unique constraint is not met."""
    session: Session = empty_test_db
    user: dict[str, str] = users_mock.valid_users()[0]
    user1: dict[str, str] = users_mock.valid_users()[0]
    db_user: UserModel = UserModel.model_validate(user)
    db_user1: UserModel = UserModel.model_validate(user1)

    with pytest.raises(DatabaseError) as dbe:
        on_db: SQLModel = await Crud().post(
            datamodel=db_user,
            session= session)

        on_db1: SQLModel = await Crud().post(
            datamodel=db_user1,
            session=session)
    assert "IntegrityError" in str(dbe.value)

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
async def test_get(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Test get method."""
    session: Session = empty_test_db
    user: dict[str, str] = users_mock.valid_users()[0]
    db_user: UserModel = UserModel.model_validate(user)

    in_db: SQLModel = await Crud().post(datamodel=db_user, session=session)

    Logger().logger.debug(f"TESTING:: db_user: {db_user.username} created ::TESTING")

    on_db: SQLModel = await Crud().get(
        datamodel=UserModel,
        column="username",
        value= db_user.username,
        returnmodel= UserResponseSchema,
        session=session,
    )
    assert on_db.username == db_user.username

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
async def test_get_exception(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Test value not found in database."""
    session: Session = empty_test_db

    with pytest.raises(DatabaseError) as dbe:
        on_db: SQLModel = await Crud().get(
            datamodel=UserModel,
            column="username",
            value='wrong_username',
            returnmodel=UserResponseSchema,
            session=session,
        )
    assert 'NoResultFound' in str(dbe.value)

    with pytest.raises(DatabaseError) as dbe:
        on_db: SQLModel = await Crud().get(
            datamodel=UserModel,
            column="wrong_column",
            value="dummy_user",
            returnmodel=UserResponseSchema,
            session=session,
        )
    assert "AttributeError" in str(dbe.value)

    with pytest.raises(DatabaseError) as dbe:
        on_db: SQLModel = await Crud().get(
            datamodel=UserResponseSchema,
            column="username",
            value="dummy_user",
            returnmodel=UserResponseSchema,
            session=session,
        )
    assert "ArgumentError" in str(dbe.value)

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
async def test_get_column_entries(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Test get_column_entries method."""
    session: Session = empty_test_db

    for each in users_mock.valid_users():
        db_user: UserModel = UserModel.model_validate(each)
        await Crud().post(datamodel=db_user, session=session)
        Logger().logger.debug(f"TESTING:: db_user: {db_user.username} created ::TESTING")

    userlist: list[str] = await Crud().get_column_entries(
        datamodel=UserModel,
        column="username",
        session=session,
        )
    
    assert len(userlist) == len(users_mock.valid_users())

    for each in users_mock.valid_users():
        assert each['username'] in userlist

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
async def test_get_column_entries_exception(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Test invalid column name."""
    session: Session = empty_test_db

    with pytest.raises(DatabaseError) as dbe:
        await Crud().get_column_entries(
            datamodel=UserModel,
            column="wrong_column",
            session=session,
        )

    assert 'AttributeError' in str(dbe.value)