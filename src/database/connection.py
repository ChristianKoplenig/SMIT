import os
from typing import Generator, Any
from dotenv import load_dotenv

from sqlmodel import create_engine, Session
from sqlalchemy.engine import URL
from sqlalchemy.engine.base import Engine

from utils.logger import Logger
from exceptions.db_exc import DatabaseError

# Import secrets
load_dotenv()
db_user = os.getenv("DATABASE_SMIT_USERNAME")
db_pwd = os.getenv("DATABASE_SMIT_PASSWORD")
db_host = os.getenv("DATABASE_SMIT_HOST")
db_database = os.getenv("DATABASE_SMIT_NAME")

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