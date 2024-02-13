from typing import Generator
from sqlalchemy.engine import URL
from sqlmodel import create_engine, Session

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

# Create the engine
engine = create_engine(url) #, echo=True)

def local_session() -> Session:
    """Return SqlModel session"""
    return Session(engine)

def get_db() -> Generator[Session, None, None]:
    """
    Returns a database session.

    Yields:
        SessionLocal: The database session.

    """
    db = local_session()
    try:
        yield db
    finally:
        db.close()