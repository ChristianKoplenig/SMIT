import pytest  
from sqlalchemy.exc import OperationalError
from db.db_exceptions import DbCreateError, DbEngineError

from sqlmodel import Session

from db.crud import SmitDb
from db.models import AuthModel
from utils.logger import Logger

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
    mocker.patch("db.connection.get_db", side_effect=DbEngineError('Mocked Error'))  
  
    # Test DB Connection  
    with pytest.raises(DbEngineError):  
        db = SmitDb(AuthModel, secrets)
  
# @pytest.mark.smoke
# #@pytest.mark.db_engine  
# def test_session_failure(session, 
#                          mocker,
#                          valid_users,
#                          db_instance_empty):  
#     """Test session handling.

#     Args:
#         session: The session object for database operations.
#         mocker: The mocker object for mocking database operations.
#         valid_users: A dictionary of valid user data.

#     Raises:
#         DbCreateError: If the session fails to create the instance.

#     """
#     #db = SmitDb(AuthModel, CoreApi(), secrets) 
#     db = db_instance_empty
  
#     # Correctly instantiate an OperationalError for mocking  
#     # operational_error = OperationalError(  
#     #     statement="some SQL statement",  
#     #     params={},  
#     #     orig=Exception("Session Cannot Be Created"),  
#     # )  

#     instance = db.db_schema.model_validate(valid_users['dummy_user'])
    
#     # Mock the `commit` method of the session to raise the mocked OperationalError  
#     mocker.patch.object(session, "commit", side_effect=DbCreateError('Mocked Error'))  
  
#     with pytest.raises(DbCreateError): 
#         with session as session: 
#             db.create_instance(instance)

# @pytest.mark.smoke
# #@pytest.mark.db_engine
# def test_session_failure_ai(session, mocker, valid_users, db_instance_empty):
#     # Mock the Session object
#     mocked_session = mocker.MagicMock(spec=Session)
    
#     # Configure the mocked session behavior
#     mocked_session.add.return_value = None
#     mocked_session.commit.side_effect = DbCreateError('Mocked Error')
    
#     # Patch the Session object in the SmitDb class with the mocked session
#     mocker.patch.object(Session, 'commit', return_value=mocked_session)
    
#     # Your test code here
#     db = db_instance_empty
#     instance = db.db_schema.model_validate(valid_users['dummy_user'])
    
#     with pytest.raises(DbCreateError):

#         db.create_instance(instance)
