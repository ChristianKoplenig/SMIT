import pytest  
from sqlalchemy.exc import OperationalError
from db.db_exceptions import DbCreateError, DbEngineError

from db.smitdb import SmitDb
from db.schemas import AuthenticationSchema
from smit.smit_api import SmitApi

from . import db_test_secrets as secrets
  

@pytest.mark.smoke
@pytest.mark.db_engine  
def test_db_engine_connection(mocker):  
    """Test creation of engine.

    Args:
        mocker: The mocker object used for patching the create_engine function.

    Raises:
        DbEngineError: If the create_engine function raises a DbEngineError.

    """
    # Simulate Engine Error  
    mocker.patch("db.smitdb.create_engine", side_effect=DbEngineError('Mocked Error'))  
  
    # Test DB Connection  
    with pytest.raises(DbEngineError):  
        db = SmitDb(AuthenticationSchema, SmitApi(), secrets)
  
@pytest.mark.smoke
@pytest.mark.db_engine  
def test_session_failure(session, mocker, valid_users):  
    """Test session handling.

    Args:
        session: The session object for database operations.
        mocker: The mocker object for mocking database operations.
        valid_users: A dictionary of valid user data.

    Raises:
        DbCreateError: If the session fails to create the instance.

    """
    db = SmitDb(AuthenticationSchema, SmitApi(), secrets) 
  
    # Correctly instantiate an OperationalError for mocking  
    operational_error = OperationalError(  
        statement="some SQL statement",  
        params={},  
        orig=Exception("Session Cannot Be Created"),  
    )  

    instance = db.db_schema.model_validate(valid_users['dummy_user'])
    
    # Mock the `commit` method of the session to raise the mocked OperationalError  
    mocker.patch.object(session, "commit", side_effect=operational_error)  
  
    with pytest.raises(DbCreateError): 
        with session: 
            db.create_instance(instance)
