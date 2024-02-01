

from sqlalchemy import inspect
import pytest
from src.db.smitdb import SmitDb
from src.db.schemas import AuthenticationSchema

from src.smit.smit_api import SmitApi
from . import db_test_secrets as test_secrets

from sqlmodel import SQLModel, select, Session

class TestSmitDb(SmitDb):
    __test__ = False
    """
    Test class for the SmitDb class.

    Args:
        SmitDb (Database): _description_
    """
    def __init__(self) -> None:
        super().__init__(schema=AuthenticationSchema,
                         api=SmitApi(),
                         secrets=test_secrets)


@pytest.fixture(name='smitdb')
def test_db() -> TestSmitDb:
    """Fixture for the SmitDb class.

    Returns:
        TestSmitDb: Instance of the SmitDb class.
    """
    db = TestSmitDb()
    
    yield db
    
    SQLModel.metadata.drop_all(db.engine)
    
@pytest.fixture
def invalid_users() -> list[dict[str, str]]:
    # Mock users that fail AuthenticationSchema validation
    return [
        # Empty username
        {
            'username': '',
            'password': '$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om',
            'email': 'dummy@dummymail.com',
            'sng_username': 'dummy_sng_login',
            'sng_password': 'dummy_sng_password',
            'daymeter': '199996',
            'nightmeter': '199997'
        },
        # Empty password
        {
            'username': 'dummy_user',
            'password': '',
            'email': 'dummy@dummymail.com',
            'sng_username': 'dummy_sng_login',
            'sng_password': 'dummy_sng_password',
            'daymeter': '199996',
            'nightmeter': '199997'
        },
        # Meters fail
        {
            'username': 'dummy_user',
            'password': '$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om',
            'email': 'dummy@dummymail.com',
            'sng_username': 'dummy_sng_login',
            'sng_password': 'dummy_sng_password',
            'daymeter': 'morethansix',
            'nightmeter': '199'
        }
    ]

@pytest.mark.smoke
#@pytest.mark.database
def test_create_table(smitdb) -> None:
    """Test initialization of the database table.

    Args:
        test_db (TestSmitDb): Instance of the SmitDb class.
    """
    smitdb.create_table()
    
    inspector = inspect(smitdb.engine)
    
    assert 'auth_dev' in inspector.get_table_names()
    
    
@pytest.mark.smoke
#@pytest.mark.database
def test_create_instance(smitdb: SmitDb) -> None:
    
    user = {
        'username': 'dummy_user',
        'password': '$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om',
        'email': 'dummy@dummymail.com',
        'sng_username': 'dummy_sng_login',
        'sng_password': 'dummy_sng_password',
        'daymeter': '199996',
        'nightmeter': '199997'
    }
    
    instance = AuthenticationSchema.model_validate(user)
    
    smitdb.create_table()
    
    smitdb.create_instance(instance)
    
 # Verify that the instance is added to the database
    with Session(smitdb.engine) as session:
        result = session.exec(select(AuthenticationSchema)).all()
        assert len(result) == 1
        assert result[0].username == 'dummy_user'

@pytest.mark.database
def test_create_invalid_instance(smitdb: SmitDb, invalid_users, capsys) -> None:
    
    smitdb.create_table()
    
    for user in invalid_users:
        
        print(f"Testing user: {user}")
        #with pytest.raises(ValueError):
        #     instance = AuthenticationSchema.model_validate(user)
        #     smitdb.create_instance(instance)
        try:
            instance = AuthenticationSchema.model_validate(user)
            smitdb.create_instance(instance)
        except Exception as e:
            print(f"Failed to create user: {e}")
            
        # Capture the output
        # captured = capsys.readouterr()
        # print(captured.out)
            
            
    # Verify that the instance is not added to the database
    with Session(smitdb.engine) as session:
        result = session.exec(select(AuthenticationSchema)).all()
        assert len(result) == 0
      

# @pytest.mark.database
# @pytest.mark.parametrize('user', [
#     {
#         'username': 'user1',
#         'password': 'password1',
#         'email': 'email1@example.com',
#         'sng_username': 'sng_user1',
#         'sng_password': 'sng_password1',
#         'daymeter': '100',
#         'nightmeter': '200'
#     },
#     {
#         'username': 'user2',
#         'password': 'password2',
#         'email': 'email2@example.com',
#         'sng_username': 'sng_user2',
#         'sng_password': 'sng_password2',
#         'daymeter': '300',
#         'nightmeter': '400'
#     },
#     # Add more users as needed
# ])
# def test_create_invalid_instance(smitdb: SmitDb, capsys, user) -> None:
    
#     smitdb.create_table()
    
#     print(f"Testing user: {user}")
#     try:
#         instance = AuthenticationSchema.model_validate(user)
#         smitdb.create_instance(instance)
#     except Exception as e:
#         print(f"Failed to create user: {e}")
        
#     # Capture the output
#     captured = capsys.readouterr()
#     print(captured.out)
        
#     # Verify that the instance is not added to the database
#     with Session(smitdb.engine) as session:
#         result = session.exec(select(AuthenticationSchema)).all()
#         assert len(result) == 0  
