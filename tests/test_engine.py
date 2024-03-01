import pytest
from typing import Callable
#from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError

from database.connection import local_session, DatabaseError, Session

@pytest.mark.smoke
@pytest.mark.engine
def test_local_session_exception(mocker: Callable) -> None:
    """Test database error exception when creating a local session."""
    # Mock Session to raise an exception when called
    mocker.patch.object(Session, "__init__", side_effect=SQLAlchemyError)

    # Check if local_session raises a DatabaseError
    with pytest.raises(DatabaseError) as exc_info:
        local_session()

    assert "local session" in str(exc_info.value)