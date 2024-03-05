from typing import Any, Generator, Annotated
import os
from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient

from sqlmodel import Session
from sqlalchemy.engine import URL

from database.connection import Db
from database.db_setup import DbAdmin
from database.db_models import UserModel
from utils.logger import Logger

from api.main import app
from api.routes.crud import dep_get_db

load_dotenv()
db_user: str | None = os.getenv("DATABASE_SMIT_USERNAME")
db_pwd: str | None = os.getenv("DATABASE_SMIT_PASSWORD")
db_host: str | None = os.getenv("DATABASE_SMIT_HOST")
db_database: str | None = os.getenv("TEST_DATABASE_SMIT_NAME")

testing_url: URL = URL.create(
    drivername="postgresql+psycopg",
    username=db_user,
    host=db_host,
    database=db_database,
    password=db_pwd,
)

@pytest.fixture
def db_test_instance(scope='session') -> Generator[Db, Any, None]:
    """Connect to test database."""
    db = Db(url=testing_url)
    Logger().logger.debug("Creating test database instance")
    yield db
    db.engine.dispose()
    Logger().logger.debug("Disposing test database instance")

@pytest.fixture
def db_test_session(
    db_test_instance: Annotated[Db, 'Connection to test database.'],
    scope='session'
) -> Generator[Session, Any, None]:
    """Yield test database session."""
    testing_session = Session(db_test_instance.db_engine())
    Logger().logger.debug("Opening test database session")
    yield testing_session
    Logger().logger.debug("Closing test database session")
    testing_session.close()

@pytest.fixture
def empty_test_db(
    db_test_instance: Annotated[Db, "Connection to test database."],
    db_test_session: Annotated[Session, "Test database session."],
    scope="function",
) -> Generator[Db, Any, None]:
    """Yield clean test database."""
    try:
        DbAdmin().create_table(engine=db_test_instance.db_engine())
        DbAdmin().delete_all(session=db_test_session, db_model=UserModel)
        yield db_test_instance
    finally:
        DbAdmin().delete_all(session=db_test_session, db_model=UserModel)

@pytest.fixture
def api_testclient(
    db_test_session: Session
) -> Generator[TestClient, Any, None]:
    """Instantiate fastapi test client with test database session.
    """
    session: Session = db_test_session

    def override_get_db() -> Generator[Session, Any, None]:
        try:
            Logger().logger.debug("Using testclient with test session")
            yield session
        finally:
            Logger().logger.debug("Closing testclient test session")
            session.rollback()
            session.close()
    
    app.dependency_overrides[dep_get_db] = override_get_db
    test_client = TestClient(app)

    DbAdmin().delete_all(session=db_test_session, db_model=UserModel)

    Logger().logger.debug("Yielding test client")
    try:
        yield test_client
    finally:
        DbAdmin().delete_all(session=db_test_session, db_model=UserModel)
        Logger().logger.debug("Closing test client")