"""Test database users_crud directly."""
import pytest
from typing import Annotated
from sqlmodel import Session, SQLModel

from database.crud import Crud
from database.db_models import UserModel
from schemas.user_schemas import UserResponseSchema, UserUpdateSchema
from exceptions.db_exc import DatabaseError

from utils import users_mock
from utils.logger import Logger

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
async def test_post(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Use UserModel to test post method.

    Asserts:
        The username on the database.
        The email on the database.
        The daymeter on the database.
    """
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
    """Test for database error when username unique constraint is not met.
    
    Asserts:
        DatabaseError: 'IntegrityError' in the exception message.
    """
    session: Session = empty_test_db
    user: dict[str, str] = users_mock.valid_users()[0]
    user1: dict[str, str] = users_mock.valid_users()[0]
    db_user: UserModel = UserModel.model_validate(user)
    db_user1: UserModel = UserModel.model_validate(user1)

    with pytest.raises(DatabaseError) as dbe:
        await Crud().post(
            datamodel=db_user,
            session= session)

        await Crud().post(
            datamodel=db_user1,
            session=session)
    assert "IntegrityError" in str(dbe.value)

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
async def test_get(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Use UserModel to test read method.
    
    Asserts:
        Get method returns correct username from database.
    """
    session: Session = empty_test_db
    user: dict[str, str] = users_mock.valid_users()[0]
    db_user: UserModel = UserModel.model_validate(user)

    await Crud().post(datamodel=db_user, session=session)

    Logger().logger.debug(
        f"TESTING:: db_user: {db_user.username} created ::TESTING")

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
    """Exception tests for get method.
    
    Asserts:
        DatabaseError: 'NoResultFound' for wrong_username.
        DatabaseError: 'AttributeError' for wrong_column.
        DatabaseError: 'ArgumentError' for wrong datamodel.
    """
    session: Session = empty_test_db

    with pytest.raises(DatabaseError) as dbe:
        await Crud().get(
            datamodel=UserModel,
            column="username",
            value='wrong_username',
            returnmodel=UserResponseSchema,
            session=session,
        )
    assert 'NoResultFound' in str(dbe.value)

    with pytest.raises(DatabaseError) as dbe:
        await Crud().get(
            datamodel=UserModel,
            column="wrong_column",
            value="dummy_user",
            returnmodel=UserResponseSchema,
            session=session,
        )
    assert "AttributeError" in str(dbe.value)

    with pytest.raises(DatabaseError) as dbe:
        await Crud().get(
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
    """Test get_column_entries method.
    
    Asserts:
        The number of users in the database.
        Compare usernames from database against local.
    """
    session: Session = empty_test_db

    for each in users_mock.valid_users():
        db_user: UserModel = UserModel.model_validate(each)
        await Crud().post(datamodel=db_user, session=session)
        Logger().logger.debug(
            f"TESTING:: db_user: {db_user.username} created ::TESTING")

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
    """Exception tests for get_column_entries method.
    
    Asserts:
        DatabaseError: 'AttributeError' for wrong_column.
    """
    session: Session = empty_test_db

    with pytest.raises(DatabaseError) as dbe:
        await Crud().get_column_entries(
            datamodel=UserModel,
            column="wrong_column",
            session=session,
        )
    assert 'AttributeError' in str(dbe.value)

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
async def test_put(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Test update method.
    
    Asserts:
        Original username and modified username from database.
    """
    session: Session = empty_test_db
    user: dict[str, str] = users_mock.valid_users()[0]
    db_user: UserModel = UserModel.model_validate(user)

    in_db: SQLModel = await Crud().post(datamodel=db_user, session=session)

    Logger().logger.debug(
        f"TESTING:: db_user: {db_user.username} created ::TESTING")

    # Fetch user from database
    on_db: SQLModel = await Crud().get(
        datamodel=UserModel,
        column="id",
        value= in_db.id,
        returnmodel=UserResponseSchema,
        session=session,
    )
    Logger().logger.debug(
        f"TESTING:: Original username: {on_db.username} ::TESTING")

    # Update username
    await Crud().put(
        datamodel=UserModel,
        select_column="id",
        select_value=in_db.id,
        update_entry="username",
        update_value="new_username",
        returnmodel=UserResponseSchema,
        session=session,
    )

    # Get modified user from database
    updated_db: SQLModel = await Crud().get(
        datamodel=UserModel,
        column="id",
        value=in_db.id,
        returnmodel=UserResponseSchema,
        session=session,
    )
    Logger().logger.debug(
        f"TESTING:: Modified username: {updated_db.username} ::TESTING")

    assert updated_db.username == "new_username"

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
async def test_put_exception(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Exception tests for update method.
    
    Asserts:
        DatabaseError: 'ValidationError' for Pydantic field validation error.
        DatabaseError: 'ValueError' for wrong database entry field.
        DatabaseError: 'AttributeError' for wrong_column.

    """
    session: Session = empty_test_db
    user: dict[str, str] = users_mock.valid_users()[0]
    db_user: UserModel = UserModel.model_validate(user)

    in_db: SQLModel = await Crud().post(datamodel=db_user, session=session)

    Logger().logger.debug(
        f"TESTING:: db_user: {db_user.username} created ::TESTING")

    with pytest.raises(DatabaseError) as dbe:
        await Crud().put(
            datamodel=UserModel,
            select_column="id",
            select_value=in_db.id,
            update_entry="username",
            update_value="new",
            returnmodel=UserResponseSchema,
            session=session,
        )
    assert 'ValidationError' in str(dbe.value)

    with pytest.raises(DatabaseError) as dbe:
        await Crud().put(
            datamodel=UserModel,
            select_column="id",
            select_value=in_db.id,
            update_entry="wrong_entry",
            update_value="new_username",
            returnmodel=UserResponseSchema,
            session=session,
        )
    assert "ValueError" in str(dbe.value)

    with pytest.raises(DatabaseError) as dbe:
        await Crud().put(
            datamodel=UserModel,
            select_column="wrong_column",
            select_value=in_db.id,
            update_entry="username",
            update_value="new_username",
            returnmodel=UserResponseSchema,
            session=session,
        )
    assert "AttributeError" in str(dbe.value)

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
async def test_delete(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Test delete method.
    
    Asserts:
        Username not in userlist from database.
    """
    session: Session = empty_test_db
    user: dict[str, str] = users_mock.valid_users()[0]
    user1: dict[str, str] = users_mock.valid_users()[1]
    db_user: UserModel = UserModel.model_validate(user)
    db_user1: UserModel = UserModel.model_validate(user1)

    await Crud().post(datamodel=db_user, session=session)
    await Crud().post(datamodel=db_user1, session=session)

    Logger().logger.debug(f"TESTING:: db_user: {db_user.username} created ::TESTING")
    Logger().logger.debug(f"TESTING:: db_user: {db_user1.username} created ::TESTING")

    await Crud().delete(
        datamodel=UserModel,
        column="username",
        value="dummy_user",
        session=session,
    )

    userlist: list[str] = await Crud().get_column_entries(
        datamodel=UserModel,
        column="username",
        session=session,
    )
    assert 'dummy_user' not in userlist

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
async def test_delete_exception(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Exception tests for delete method.
    
    Asserts:
        DatabaseError: 'NoResultFound' for value search pattern.
        DatabaseError: 'AttributeError' for column not found on database.
    """
    session: Session = empty_test_db
    user: dict[str, str] = users_mock.valid_users()[0]
    db_user: UserModel = UserModel.model_validate(user)

    await Crud().post(datamodel=db_user, session=session)

    Logger().logger.debug(
        f"TESTING:: db_user: {db_user.username} created ::TESTING")

    with pytest.raises(DatabaseError) as dbe:
        await Crud().delete(
            datamodel=UserModel,
            column="username",
            value="wrong_username",
            session=session,
        )
    assert "NoResultFound" in str(dbe.value)

    with pytest.raises(DatabaseError) as dbe:
        await Crud().delete(
            datamodel=UserModel,
            column="wrong_column",
            value="dummy_user",
            session=session,
        )
    assert "AttributeError" in str(dbe.value)

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.crud
@pytest.mark.dev
async def test_patch(
    empty_test_db: Annotated[Session, "Database session"],
) -> None:
    """Test update method.

    Asserts:
        Sng_username and daymeter from database.
        Id not changed.
    """
    session: Session = empty_test_db
    user: dict[str, str] = users_mock.valid_users()[0]
    db_user: UserModel = UserModel.model_validate(user)

    in_db: SQLModel = await Crud().post(datamodel=db_user, session=session)

    Logger().logger.debug(f"TESTING:: db_user: {db_user.username} created ::TESTING")

    # Fetch user from database
    on_db: SQLModel = await Crud().get(
        datamodel=UserModel,
        column="id",
        value=in_db.id,
        returnmodel=UserResponseSchema,
        session=session,
    )
    Logger().logger.debug(f"TESTING:: Original username: {on_db.sng_username} ::TESTING")

    new_data: UserUpdateSchema = UserUpdateSchema(
        sng_username="new_username",
        daymeter=123456)

    # Update username
    await Crud().patch(
        column="id",
        value=in_db.id,
        datamodel=UserModel,
        new_data=new_data,
        session=session,
    )

    # Get modified user from database
    updated_db: SQLModel = await Crud().get(
        datamodel=UserModel,
        column="id",
        value=in_db.id,
        returnmodel=UserResponseSchema,
        session=session,
    )
    Logger().logger.debug(
        f"TESTING:: Modified username: {updated_db.sng_username} ::TESTING"
    )

    assert updated_db.sng_username == "new_username"
    assert updated_db.daymeter == 123456
    assert updated_db.id == in_db.id