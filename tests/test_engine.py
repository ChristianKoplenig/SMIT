import pytest
from typing import Callable
from sqlalchemy.exc import TimeoutError, OperationalError
from sqlmodel import Session

from database.connection import Db
from database.crud import Crud
from database.db_models import UserModel
from utils.users_mock import valid_users

from exceptions.db_exc import DatabaseError

@pytest.mark.smoke
@pytest.mark.engine
def test_create_engine_error(mocker: Callable) -> None:
    """Simulate a timeout error when creating an engine.

    This test case uses the `mocker` fixture to patch the `create_engine` function
    from the `database.connection` module. The patched function is set to raise a
    `TimeoutError` when called.

    The test then checks if calling `Db().db_engine()` raises a `DatabaseError`,
    indicating that the timeout error was properly handled.

    Raises:
        DatabaseError: 
            Fails if calling `Db().db_engine()` does not raise a `DatabaseError`.
    """
    mocker.patch("database.connection.create_engine", side_effect=TimeoutError)

    # Check for TimeOutError
    with pytest.raises(DatabaseError):
        Db().db_engine()

@pytest.mark.asyncio
@pytest.mark.smoke
@pytest.mark.engine
async def test_session_failure(
    db_test_session: Session,
    mocker: Callable,
) -> None:
    """Test session failure.

    Args:
        db_test_session (Session): The test session object.
        mocker (Callable): The mocker object for patching.

    Raises:
        DatabaseError: 
            Fails if the `Crud().post()` method does not raise a `DatabaseError`.
    """

    db = Crud()
    session: Session = db_test_session

    # Correctly instantiate an OperationalError for mocking
    operational_error = OperationalError(
        statement="some SQL statement",
        params={},
        orig=Exception("Session Cannot Be Created"),
    )

    user: UserModel = UserModel.model_validate(valid_users()[0])

    # Mock the `commit` method of the session to raise the mocked OperationalError
    mocker.patch.object(session, "commit", side_effect=operational_error)

    with pytest.raises(DatabaseError):
        await db.post(datamodel=user, session=session)
