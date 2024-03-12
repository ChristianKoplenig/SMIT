from typing import Any, Generator, Annotated
import os
from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient

from sqlmodel import Session
from sqlalchemy.engine import URL
from sqlalchemy.engine.base import Engine

from database.connection import Db
from database.db_admin import DbAdmin
from database.db_models import UserModel
from utils.logger import Logger

from api.main import app
from api.dependencies import dep_session

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

@pytest.fixture(scope='session')
def db_test_instance() -> Generator[Db, Any, None]:
    """Connect to test database."""
    db: Db = Db(url=testing_url)
    yield db

@pytest.fixture(scope='session')
def db_test_engine(
    db_test_instance: Annotated[Db,
                                "Database instance for test connection."],
) -> Generator[Engine, Any, None]:
    engine: Engine = db_test_instance.db_engine()
    Logger().logger.debug(
        f'Test engine for database: "{testing_url.database}" established.')
    yield engine
    Logger().logger.debug(
        f'Disposing test engine for database: "{testing_url.database}".')
    engine.dispose()

@pytest.fixture(scope='function')
def db_test_session(
    db_test_engine: Annotated[Engine,
                              "Engine connected to test database."],
) -> Generator[Session, Any, None]:
    """Yield test database session."""
    testing_session: Session = Session(db_test_engine)
    Logger().logger.debug(
        f'Test session connected to database: "{testing_url.database}".')
    yield testing_session
    Logger().logger.debug(
        f'Closing test session for database: "{testing_url.database}".')
    testing_session.close()

@pytest.fixture(scope='function')
def empty_test_db(
    db_test_session: Annotated[Session,
                               "Test database session."],
    db_test_engine: Annotated[Engine,
                              "Engine connected to test database."],
) -> Generator[Session, Any, None]:
    """Yield clean test database."""

    DbAdmin().create_table(engine=db_test_engine)
    DbAdmin().delete_all(session=db_test_session, db_model=UserModel)
    empty_instance: Session = db_test_session
    try:
        yield empty_instance
    finally:
        DbAdmin().delete_all(session=empty_instance, db_model=UserModel)
        Logger().logger.debug(
            f'Closing test connection to table: "{UserModel.__tablename__}".')
        empty_instance.close()

@pytest.fixture(scope='function')
def api_testclient(
    db_test_session: Annotated[Session,
                               "Test database session."],
) -> Generator[TestClient, Any, None]:
    """Instantiate fastapi test client with test database session.
    """
    session: Session = db_test_session

    def override_get_db() -> Generator[Session, Any, None]:
        try:
            Logger().logger.debug("Using testclient with test session.")
            yield session
        finally:
            Logger().logger.debug("Closing testclient test session.")
            session.rollback()
            session.close()
    
    app.dependency_overrides[dep_session] = override_get_db
    test_client: Annotated[TestClient, 'FastApi TestClient'] = TestClient(app)

    DbAdmin().delete_all(session=db_test_session, db_model=UserModel)

    Logger().logger.debug("Yielding test client.")
    try:
        yield test_client
    finally:
        DbAdmin().delete_all(session=db_test_session, db_model=UserModel)
        Logger().logger.debug("Closing test client.")