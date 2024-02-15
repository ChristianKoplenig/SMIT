from typing import Generator, Any
import contextlib

from sqlmodel import create_engine, Session
from sqlalchemy.engine import URL
from sqlalchemy.engine.base import Engine

from utils.logger import Logger

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
    """Return SqlModel session"""
    return Session(engine)

def get_db() -> Generator[Session, Any, None]:
    """Return database session for fastapi.

    Connect to smit database at fly.io.

    Yields:
        SessionLocal: Develop connection to fly.io postgres database.

    """
    db: Session = local_session()
    try:
        Logger().logger.debug("Opening database session")
        yield db
    finally:
        Logger().logger.debug("Closing database session")
        db.close()

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
    finally:
        Logger().logger.debug("Closing sqlalchemy session")
        session.close()