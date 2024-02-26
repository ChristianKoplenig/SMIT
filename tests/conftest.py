from typing import Any, Generator, Type
import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session, select, create_engine, SQLModel
from sqlmodel.sql.expression import SelectOfScalar
from sqlalchemy.engine import URL, ScalarResult


# Custom imports
from db.models import AuthModel
from api.schemas import UserModel
from db.crud import SmitDb
from utils.logger import Logger

from api.main import app
from db.connection import get_db

from . import db_test_secrets as secrets
class TestSmitDb(SmitDb):
    """Connect to test database.
    
    Connect to test_smit database at fly.io.

    Args:
        SmitDb (Class): Database connection and crud operations.
    """
    __test__ = False
    
    def __init__(self, schema: Type[SQLModel]= AuthModel):
        super().__init__(schema=schema)
        
        db_user = secrets.username
        db_pwd = secrets.password
        db_host = secrets.host
        self.db_database = secrets.database

        url = URL.create(
            drivername="postgresql+psycopg",
            username=db_user,
            host=db_host,
            database=self.db_database,
            password=db_pwd)
        
        self.engine = create_engine(url)
        
    def delete_all_entries(self, session: Session) -> None:
        """
        Delete all entries from the database.

        Args:
            session (Session): SqlModel session.

        Returns:
            None
        """
        statement: SelectOfScalar[SQLModel] = select(self.db_schema)
        results: ScalarResult[SQLModel] = session.exec(statement)
        
        for each in results:
            session.delete(each)
            session.commit()
            self.logger.debug('Deleted row %s', each.username)

### Setup for database module testing ###
@pytest.fixture(scope="session")  
def db_instance() -> Generator[TestSmitDb, Any, None]:  
    """Create connection to smit test database.  
    """  
    db = TestSmitDb()
    yield db  

@pytest.fixture(scope="session")
def test_session(db_instance: TestSmitDb) -> Generator[Session, Any, None]:
    """Yield a SqlModel Session with TestSmitDb connection.  
    """  
    session = Session(db_instance.engine)  
    Logger().logger.debug("Opening database test_session")
    yield session  
    Logger().logger.debug("Closing database test_session")
    session.close()

@pytest.fixture(scope="function")  
def db_instance_empty(db_instance: TestSmitDb,
                      test_session: Session) -> Generator[TestSmitDb, Any, None]:  
    """Yield clean authentication table.  
    """  
    # Clear DB before test function  
    db_instance.create_table(db_instance.engine)
    db_instance.delete_all_entries(session=test_session)  
    
    yield db_instance  

    db_instance.delete_all_entries(session=test_session)

### Setup for fastapi module testing ###
@pytest.fixture(scope="session")
def api_instance() -> Generator[TestSmitDb, Any, None]:
    """Setup SmitDb crud operations for testing.
    
    Mock SmitDb class to connect to test database.
    Load SmitDb with API table schema.
    Provide crud operations from SmitDb for testing.

    Yields:
        TestSmitDb: SmitDb class with testing connection.
    """
    db = TestSmitDb(schema=UserModel)
    yield db

@pytest.fixture(scope="session")
def api_test_session(api_instance: TestSmitDb) -> Generator[Session, Any, None]:
    """Yield SmitDb testing session."""
    session = Session(api_instance.engine)
    Logger().logger.debug("Opening database api_test_session")
    yield session
    Logger().logger.debug("Closing database api_test_session")
    session.close()

@pytest.fixture(scope="function")
def api_instance_empty(
    api_instance: TestSmitDb, api_test_session: Session
) -> Generator[TestSmitDb, Any, None]:
    """Yield clean authentication table.

    This function is a fixture that yields the SmitDb class 
    in testing setup.
    It clears the database before the test function is executed 
    and deletes all entries after the test function is executed.

    Args:
        api_instance (TestSmitDb): Instance of SmitDb class in testing setup.
        api_test_session (Session): The database session.

    Yields:
        TestSmitDb: A clean instance of the SmitDb testing class.

    """
    # Clear DB before test function
    api_instance.create_table(api_instance.engine)
    api_instance.delete_all_entries(session=api_test_session)

    yield api_instance

    api_instance.delete_all_entries(session=api_test_session)

@pytest.fixture
def test_app(api_test_session: Session) -> Generator[TestClient, Any, None]:
    """Yield TestClient instance with get_db override.

    Use test database for testing.

    Args:
        test_session (Session): The test session database session.

    Yields:
        TestClient: TestClient instance for fastapi testing.

    """
    session: Session = api_test_session

    def override_get_db() -> Generator[Session, Any, None]:
        try:
            Logger().logger.debug("Opening override session")
            yield session
        finally:
            Logger().logger.debug("Closing override session")
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client

@pytest.fixture
def invalid_users() -> Generator[dict[str, dict[str, str]], None, None]:
    """Generate a dictionairy of invalid user data.
    
    Returns a dict with key:value pairs holding invalid user data.
            
    Yields:
        dict[str, dict[str, str]]: A dictionary representing an invalid user.
    """
    no_username: dict[str, str] = {
            'username': '',
            'password': '$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om',
            'email': 'dummy@dummymail.com',
            'sng_username': 'dummy_sng_login',
            'sng_password': 'dummy_sng_password',
            'daymeter': '199996',
            'nightmeter': '199997'
        }
    short_username: dict[str, str] = {
        "username": "abc",
        "password": "$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om",
        "email": "dummy@dummymail.com",
        "sng_username": "dummy_sng_login",
        "sng_password": "dummy_sng_password",
        "daymeter": "199996",
        "nightmeter": "199997",
    }
    empty_pwd: dict[str, str] ={
            'username': 'dummy_user',
            'password': '',
            'email': 'dummy@dummymail.com',
            'sng_username': 'dummy_sng_login',
            'sng_password': 'dummy_sng_password',
            'daymeter': '199996',
            'nightmeter': '199997'
        }
    meter_string: dict[str, str] = {
            'username': 'dummy_user',
            'password': '$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om',
            'email': 'dummy@dummymail.com',
            'sng_username': 'dummy_sng_login',
            'sng_password': 'dummy_sng_password',
            'daymeter': 'morethansix',
            'nightmeter': '199996'
        }
    meter_short: dict[str, str] = {
            'username': 'dummy_user',
            'password': '$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om',
            'email': 'dummy@dummymail.com',
            'sng_username': 'dummy_sng_login',
            'sng_password': 'dummy_sng_password',
            'daymeter': '123',
            'nightmeter': '199996'
        }
    mail_invalid: dict[str, str] = {
            'username': 'dummy_user',
            'password': '$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om',
            'email': 'dummydummymail.com',
            'sng_username': 'dummy_sng_login',
            'sng_password': 'dummy_sng_password',
            'daymeter': '199997',
            'nightmeter': '199996'
        }
    sng_user_short: dict[str, str] = {
        "username": "dummy_user",
        "password": "$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om",
        "email": "dummy@dummymail.com",
        "sng_username": "sng",
        "sng_password": "dummy_sng_password",
        "daymeter": "199997",
        "nightmeter": "199996",
    }
    fail_users: dict[str, dict[str, str]] = {
        'no_username': no_username,
        'short_username': short_username,
        'empty_password': empty_pwd,
        'mail_invalid': mail_invalid,
        'meter_string': meter_string,
        'meter_short': meter_short,
        'sng_user_short': sng_user_short
    }
    yield fail_users

@pytest.fixture
def valid_users() -> Generator[dict[str, dict[str, str | int]], None, None]:
    """Generate a dictionary of valid user data.
    
    Returns a dict with key:value pairs from `AuthModel` class.
    
    Returns:
        dict[str, str]: A dictionary containing valid user information.
    """
    user1: dict[str, str | int] = {
        "username": "dummy_user",
        "password": "$argon2id$v=19$m=65536,t=3,p=4$NxWNf7Vxcwv3I25r6T9TZQ$aSw0+lmoZPsaildOr93ted9qR/UQ3moG5pokYb9HEZo",
        "email": "dummy@dummymail.com",
        "sng_username": "dummy_sng_login",
        "sng_password": "dummy_sng_password",
        "daymeter": 199996,
        "nightmeter": 199997,
    }
    
    user2: dict[str, str | int] = {
        "username": "dummy_user2",
        "password": "$argon2id$v=19$m=65536,t=3,p=4$5pD+VDlNiib9xXyn8l4n9g$+L5Y8qWw4Y6EriSlIeYlXpIfUiHedtZkblDNEBv3jc8",
        "email": "dummy2@dummymail.com",
        "sng_username": "dummy2_sng_login",
        "sng_password": "dummy2_sng_password",
        "daymeter": 199994,
        "nightmeter": 199995,
    }
    
    good_users: dict[str, dict[str, str | int]] = {
        'dummy_user' : user1,
        'dummy_user2' : user2
    }
    yield good_users