from typing import Annotated, Any, Generator
import os
from dotenv import load_dotenv

from sqlmodel import Session, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.engine.base import Engine

from exceptions.db_exc import DatabaseError
from utils.logger import Logger

# Import secrets
load_dotenv()
db_user = os.getenv("DATABASE_SMIT_USERNAME")
db_pwd = os.getenv("DATABASE_SMIT_PASSWORD")
db_host = os.getenv("DATABASE_SMIT_HOST")
db_database = os.getenv("DATABASE_SMIT_NAME")

# Define database connection
url: URL = URL.create(
    drivername="postgresql+psycopg",
    username=db_user,
    host=db_host,
    database=db_database,
    password=db_pwd,
)


class Db:
    """Class to manage database connection.

    This class is used to manage the connection to the database.
    """

    def __init__(
        self,
        url: Annotated[URL, "Connection Parameters"] = url,
    ) -> None:
        """Initialize DbConnection class."""
        self.engine: Engine = create_engine(url)

        Logger().log_module_init()
        Logger().logger.debug(f'Engine for connection to "{url.database}" database created')


    def local_session(self) -> Session:
        """Return SqlModel session.

        Use engine to create a session for the smit database at fly.io.

        Returns:
            Session: SqlModel session for smit database at fly.io.
        """
        try:
            session = Session(self.engine)
            Logger().logger.debug(f'Session for "{url.database}" database created.')
            return session
        except Exception as e:
            Logger().log_exception(e)
            raise DatabaseError(e, "Error creating local session") from e

    def get_db(self) -> Generator[Session, Any, None]:
        """Return database session for fastapi.

        Use local_session() to connect to database.

        Yields:
            Session: SqlModel session for smit database at fly.io.

        """
        db: Session = self.local_session()
        try:
            Logger().logger.debug(f'Session for "{url.database}" database opened.')
            yield db
        finally:
            db.rollback()
            db.close()
            Logger().logger.debug(f'Session for "{url.database}" database closed.')

    def db_engine(self) -> Engine:
        """Return the engine for smit database at fly.io.

        Returns:
            Engine: SqlModel engine for smit database at fly.io.
        """
        return self.engine