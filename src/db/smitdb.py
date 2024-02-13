from typing import TYPE_CHECKING, Any, Optional, Sequence, Type
from sqlalchemy.engine import URL
from sqlmodel import Session, SQLModel, create_engine, select

# Custom imports
from db.db_exceptions import (
    DbExceptionLogger,
    DbEngineError,
    DbReadError,
    DbCreateError,
    DbUpdateError,
    DbDeleteError,
)

from db import smitdb_secrets as db_secrets

# Imports for type hints
if TYPE_CHECKING:
    from smit.smit_api import CoreApi


class SmitDb:
    """
    Connect and manipulate Smit database at fly.io.

    ...

    Attributes
    ----------
    SmitAuth : Type[SQLModel]
        SQLModel class representing the Smit auth table.
    engine : Engine
        SQLAlchemy engine connected to the Smit database.

    Methods
    -------
    create_tables():
        Create the tables from the schema definition.
    create_dummy_user():
        Create a dummy user in the Smit auth table.
    create_user(username, password, email=None, sng_username=None, sng_password=None, daymeter=None, nightmeter=None):
        Write a user to the Smit auth table.
    init_auth_table():
        Initializes the Smit auth table by creating the table and adding a dummy user.
    select_all():
        Select the whole table from the database and print it.
    select_username(value):
        Select row from the database and return it as a dictionary.
    select_all_usernames():
        Select all usernames from the database and return them as a list.
    delete_where(column, value):
        Select row from the database and delete.
    read_db():
        Reads the SMIT database and returns all SMIT users.
    """

    def __init__(
        self, schema: Type[SQLModel], api: "CoreApi", secrets: Any = db_secrets
    ) -> None:
        """Create engine object for database.

        DB credentials are stored in secrets.py.

        Parameters
        ----------
        schema : Type[SQLModel]
            SQLModel class schema representing the table to modify.

        api : Type[SmitApi]
            Backend Api class instance.
        """
        self.db_schema: Type[SQLModel] = schema

        db_user = secrets.username
        db_pwd = secrets.password
        db_host = secrets.host
        self.db_database = secrets.database

        url = URL.create(
            drivername="postgresql+psycopg",
            username=db_user,
            host=db_host,
            database=self.db_database,
            password=db_pwd,
        )

        # Use logger from SmitBackend
        self.backend = api
        msg = f'Db engine: "{self.__class__.__name__}" connected to '
        msg += f'schema: "{self.db_schema.__name__}" '
        msg += f'with api configuration: "{self.backend.__class__.__name__}".'

        try:
            self.engine = create_engine(url)  # , echo=True)
            self.backend.logger.debug(msg)
        except Exception as e:
            self._log_exception(e)
            raise DbEngineError(
                f"Could not create engine for {self.__class__.__name__}"
            ) from e

    def _log_exception(self, e: Exception) -> None:
        """Logs the given exception to the backend logger.

        Args:
            e (Exception): The exception to be logged.

        Returns:
            None
        """
        formatted_error_message = DbExceptionLogger().logging_input(e)
        self.backend.logger.error(formatted_error_message)

    def create_table(self) -> None:
        """Create (if not exist) all tables from SQLModel classes."""
        try:
            SQLModel.metadata.create_all(self.engine)
            self.backend.logger.debug("Created table %s at database: %s",
                                      self.db_schema.__name__,
                                      self.db_database)
        except Exception as e:
            self._log_exception(e)
            raise e

    def create_instance(
        self, schema: SQLModel, session: Optional[Session] = None
    ) -> None:
        """Use SQLModel schema to add a new entry to the database.

        Example:
            new_entry = SQLModelSchema.model_validate(entry)
            db_connection.create_instance(new_entry)

        Args:
            schema (SQLModel): The model instance representing the new entry.
        """
        if not session:
            session = Session(self.engine)

        try:
            with session:
                session.add(schema)
                session.commit()
                self.backend.logger.info(
                    "Added instance of %s to database: %s",
                    schema.__class__.__name__,
                    self.db_database
                )
                # return schema
        except Exception as e:
            self._log_exception(e)
            raise DbCreateError(
                f"Could not add instance of {schema.__class__.__name__} to database"
            ) from e

    def read_all(self, session: Optional[Session] = None) -> Sequence[SQLModel]:
        """Read all data from the connected database table.

        Example:
            for row in read_all:
                print(f'ID: {row.id}, Name: {row.username}')

        Returns:
            tuple: Each row as tuple with columns as attributes.
        """
        if not session:
            session = Session(self.engine)
        try:
            with session:
                read_all: Sequence[SQLModel] = session.exec(
                    select(self.db_schema)
                ).all()
                return read_all
        except Exception as e:
            self._log_exception(e)
            raise DbReadError(
                f"Reading data for schema {self.db_schema.__name__} failed"
            ) from e

    def read_column(
        self, column: str, session: Optional[Session] = None
    ) -> Sequence[str]:
        """Read all data in the given column.

        Args:
            column (str): The column name to read.

        Returns:
            list: Each entry for the given column.

        Raises:
            ReadError: If reading data for the column fails.
        """
        if not session:
            session = Session(self.engine)
        try:
            with session:
                statement = select(getattr(self.db_schema, column))
                all_entries: Sequence[Any] = session.exec(statement).all()
                return all_entries
        except Exception as e:
            self._log_exception(e)
            raise DbReadError(
                f'Reading column: "{column}" from schema: "{self.db_schema}" failed'
            ) from e

    def select_where(
        self, column: str, value: str, session: Optional[Session] = None
    ) -> SQLModel:
        """Select row for value found in column.

        Args:
            column (str): The column name to filter the row.
            value (str): The value to match in the specified column.

        Returns:
            Selected row as tuple.
        """
        if not session:
            session = Session(self.engine)
        try:
            with session:
                statement = select(self.db_schema).where(
                    getattr(self.db_schema, column) == value
                )
                results = session.exec(statement)
                row: SQLModel = results.one()

                self.backend.logger.debug(
                    "Selected row where %s matches %s", column, value
                )
                return row
        except Exception as e:
            self._log_exception(e)
            raise DbReadError(
                f'Selecting column: "{column}" and value: "{value}" failed'
            ) from e

    def update_where(
        self, column: str, value: str, new_value: str, session: Optional[Session] = None
    ) -> bool:
        """Update row for value found in column.

        Args:
            column (str): The column name to filter the row.
            value (str): The value to match in the specified column.
            new_value (str): The new value to write to the specified column.

        Returns:
            bool: True if update was successful, False otherwise.
        """
        if not session:
            session = Session(self.engine)
        try:
            with session:
                statement = select(self.db_schema).where(
                    getattr(self.db_schema, column) == value
                )
                results = session.exec(statement)
                row = results.one()

                setattr(row, column, new_value)
                session.add(row)
                session.commit()

                self.backend.logger.debug(
                    "Updated %s from: %s to: %s", column, value, new_value
                )
            return True
        except Exception as e:
            self._log_exception(e)
            raise DbUpdateError(
                f'In column: "{column}" select value: "{value}" update with: "{new_value}" failed'
            ) from e

    def delete_where(
        self, column: str, value: str, session: Optional[Session] = None
    ) -> None:
        """Delete row for value found in column.

        Args:
            column (str): The column name to filter the row.
            value (str): The value to match in the specified column.

        Returns:
            None
        """
        if not session:
            session = Session(self.engine)
        try:
            with session:
                statement = select(self.db_schema).where(
                    getattr(self.db_schema, column) == value
                )
                results = session.exec(statement)
                row = results.one()

                session.delete(row)
                session.commit()

                self.backend.logger.debug(
                    "Deleted row where %s matches %s", column, value
                )
        except Exception as e:
            self._log_exception(e)
            raise DbDeleteError(f'Deleting row for "{column}": "{value}" failed') from e


############ Debugging ############
# from db.schemas import AuthenticationSchema
# from smit.smit_api import SmitApi

# conn = SmitDb(AuthenticationSchema, SmitApi())
# try:
#     conn.update_where('userna', 'dummy_user',  'sdf')
# except Exception as exc:
#     print(exc)
