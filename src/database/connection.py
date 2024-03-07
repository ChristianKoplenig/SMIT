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
db_user: str | None = os.getenv("DATABASE_SMIT_USERNAME")
db_pwd: str | None = os.getenv("DATABASE_SMIT_PASSWORD")
db_host: str | None = os.getenv("DATABASE_SMIT_HOST")
db_database: str | None = os.getenv("DATABASE_SMIT_NAME")

# Define database connection
url: URL = URL.create(
    drivername="postgresql+psycopg",
    username=db_user,
    host=db_host,
    database=db_database,
    password=db_pwd,
)

class Db:
    """Provide database connection.
    
    Create an engine object using the `SqlModel` engine.
    Instantiate a `SqlModel` session object connected to the url parameters.
    Yield the session object.

    Attributes:
        url (URL): Database connection parameters.
    
    Methods:
        db_engine(): Create and return engine object for provided url.
        local_session(): Instantiate and return SqlModel session.
        get_db(): Yield database session.
    
    Yields:
        Session: SqlModel session object connected to provided url.

    Raises:
        DatabaseError: On creating engine or local session.

    """

    def __init__(
        self,
        url: Annotated[URL, "Connection Parameters"] = url,
    ) -> None:
        """Initialize database connection."""
        self.url: URL = url

        Logger().log_module_init()

        

    def db_engine(self) -> Engine:
        """Return engine object for privided url.

        Defaults to production database url.

        Returns:
            Engine: SqlModel engine connected to url parameters.

        Raises:
            DatabaseError: On error creating engine.
        """
        try:
            self.engine: Engine = create_engine(self.url)
            Logger().logger.debug(
                f'Engine connected to database "{self.url.database}".')
        except Exception as e:
            Logger().log_exception(e)
            raise DatabaseError(
                e, f'Error creating engine for "{self.url.database}"') from e
        
        return self.engine

    def local_session(self) -> Session:
        """Return SqlModel session object.

        Use engine to create a session for url parameters.

        Returns:
            Session: SqlModel session connected to url parameters.

        Raises:
            DatabaseError: On error creating local session.
        """
        try:
            session = Session(self.engine)
            Logger().logger.debug(
                f'Created session connected to database: "{self.url.database}".')
            return session
        except Exception as e:
            Logger().log_exception(e)
            raise DatabaseError(
                e, "Error creating local session") from e

    def get_db(self) -> Generator[Session, Any, None]:
        """Yield session object.

        Open and close a session object connected to the url parameters.

        Yields:
            Session: SqlModel session for url parameters.

        Raises:
            DatabaseError: On error getting database connection.
        """
        db: Session = self.local_session()
        try:
            Logger().logger.debug(
                f'Opened session connected to database: "{self.url.database}".')
            yield db

        finally:
            db.rollback()
            db.close()
            Logger().logger.debug(
                f'Closed session connected to database: "{self.url.database}".')
