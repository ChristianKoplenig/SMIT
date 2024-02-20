from typing import Generator, Any
import contextlib

from sqlmodel import create_engine, Session
from sqlalchemy.engine import URL
from sqlalchemy.engine.base import Engine

from utils.logger import Logger
from sqlalchemy.exc import InvalidRequestError
from db.db_exceptions import DatabaseError, DbReadError

from db import smitdb_secrets as secrets

# Import secrets
db_user = secrets.username
db_pwd = secrets.password
db_host = secrets.host
db_database = secrets.database

# Define database connection
url = URL.create(
    drivername="postgresql+psycopg",
    username=db_user,
    host=db_host,
    database=db_database,
    password=db_pwd,
)

# Create the engine for smit database at fly.io
engine: Engine = create_engine(url) #, echo=True)

def local_session() -> Session:
    """Return SqlModel session.

    Use engine to create a session for the smit database at fly.io.

    Returns:
        Session: SqlModel session for smit database at fly.io.
    """
    try:
        return Session(engine)
    except Exception as e:
        Logger().log_exception(e)
        raise DatabaseError(e, "Error creating local session") from e

# Connection for fastapi module
def get_db() -> Generator[Session, Any, None]:
    """Return database session for fastapi.

    Use local_session() to connect to database.

    Yields:
        Session: SqlModel session for smit database at fly.io.

    """
    db: Session = local_session()
    try:
        Logger().logger.debug("Opening database session")
        yield db
    finally:
        Logger().logger.debug("Closing database session")
        db.rollback()
        db.close()

#TODO: check if extra connection is needed
# Connection for database module
@contextlib.contextmanager
def db_session() -> Generator[Session, None, None]:
    """Return database session for sqlalchemy connection.

    Connect to smit database at fly.io.

    Yields:
        SessionLocal: Develop connection to fly.io postgres database.

    """
    session: Session = local_session()
    try:
        Logger().logger.debug("Opening sqlalchemy session")
        yield session

    except DbReadError as de:
        Logger().logger.error(f"Error in database connection: {de}")
        raise de from de
    except Exception as e:
        Logger().logger.error(f"Error in database connection: {e}")
        raise InvalidRequestError(f"Error in database connection: {e}") from e

    finally:
        Logger().logger.debug("Closing sqlalchemy session")
        session.rollback()
        session.close()