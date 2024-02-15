from typing import Any, Callable, Optional, Sequence, Type
from functools import wraps

from sqlmodel import Session, SQLModel, select
from sqlmodel.sql.expression import SelectOfScalar
from sqlalchemy.engine.result import ScalarResult

from utils.logger import Logger
from db.connection import db_session, engine

# Exceptions
from db.db_exceptions import (
    DbCreateError,
    DbDeleteError,
    DbEngineError,
    DbExceptionLogger,
    DbReadError,
    DbUpdateError,
)

from db import smitdb_secrets as db_secrets

class SmitDb:
    """CRUD operations for fastapi.

    Use SQLModel to provide CRUD operations.

    Attributes:
        db_schema (Type[SQLModel]):
            The SQLModel class schema representing the table to modify.
        logger (Logger):
            Logger class from utils module.
        db_database (str):
            The name of the database. Used for logging output.

    Methods:
        __init__(self, schema: Type[SQLModel], secrets: Any = db_secrets) -> None:
            Initializes the SmitDb object.
        with_db_session(func: Callable[..., Any]) -> Callable[..., Any]:
            Decorator function to wrap a database session around a CRUD method.
        _log_exception(self, e: Exception) -> None:
            Format and log exceptions.
        create_table(self) -> None:
            Setup database tables.
        create_instance(self, schema: SQLModel, session: Optional[Session | None] = None) -> None:
            Use SQLModel schema to add a new entry to the database.
        read_all(self, session: Optional[Session] = None) -> Sequence[SQLModel]:
            Read all data from the connected database table.
        read_column(self, column: str, session: Optional[Session | None] = None) -> Sequence[SQLModel]:
            Read all data in the given column.
        select_where(self, column: str, value: str, session: Optional[Session] = None) -> SQLModel:
            Selects a row for the value found in the column.
        update_where(self, column: str, value: str, new_value: str, session: Optional[Session] = None) -> bool:
            Updates a row for the value found in the column.
        delete_where(self, column: str, value: str, session: Optional[Session] = None) -> None:
            Deletes a row for the value found in the column.
    """
    def __init__(self,
                 schema: Type[SQLModel],
                 secrets: Any = db_secrets) -> None:
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
        self.logger = Logger().logger
        self.db_database = secrets.database # Use for logging output

        Logger().log_module_init()

    @staticmethod
    def with_db_session(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Session | None:
            if kwargs.get("session") is None:
                with db_session() as session:
                    Logger().logger.debug("Wrapping session around CRUD method")
                    return func(*args, session=session, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper

    def _log_exception(self, e: Exception) -> None:
        """Format and log exceptions.

        Args:
            e (Exception): The exception to be logged.

        Returns:
            None
        """
        formatted_error_message = DbExceptionLogger().logging_input(e)
        self.logger.error(formatted_error_message)

    def create_table(self) -> None:
        """Setup database tables.
        
        Use SQLModel metadata to create all tables from SQLModel classes.

        """
        try:
            SQLModel.metadata.create_all(engine)
            self.logger.debug(
                "Created table %s at database: %s",
                self.db_schema.__name__,
                self.db_database,
            )
        except Exception as e:
            self._log_exception(e)
            raise e

    @with_db_session
    def create_instance(
        self, schema: SQLModel, session: Optional[Session | None] = None
    ) -> None:
        """Use SQLModel schema to add a new entry to the database.

        Args:
            schema (SQLModel): 
                The model instance representing the new entry.
            session (Optional[Session | None], optional): 
                The database session. Defaults to use with decorator.

        Returns:
            None
        
        Raises:
            DbCreateError: If adding the new instance to the database fails.

        Example:
            
        ```
            new_entry = SQLModelSchema.model_validate(entry)
            db_connection.create_instance(new_entry)
        ```

        """
        if session is None:
            raise DbEngineError("No session provided for create_instance")

        try:
            with session:
                session.add(schema)
                session.commit()
                self.logger.info(
                    "Added instance of %s to database: %s",
                    schema.__class__.__name__,
                    self.db_database,
                )
        except Exception as e:
            self._log_exception(e)
            raise DbCreateError(
                f"Could not add instance of {schema.__class__.__name__} to database"
            ) from e

    @with_db_session
    def read_all(self, session: Optional[Session] = None) -> Sequence[SQLModel]:
        """Read all data from the connected database table.

        Args:
            session (Optional[Session], optional): 
                The database session. Defaults to use with decorator.

        Returns:
            tuple: Each row as tuple with columns as attributes.

        Raises:
            ReadError: If reading data from the database fails.

        Example:

        ```
            for row in read_all:
                print(f'ID: {row.id}, Name: {row.username}')
        ```
        """
        if not session:
            raise DbEngineError("No session provided for read_all")

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

    @with_db_session
    def read_column(
        self, column: str, session: Optional[Session | None] = None
    ) -> Sequence[SQLModel]:
        """Read all data in the given column.

        Args:
            column (str): The column name to read.
            session (Optional[Session | None], optional):
                Defaults to use with decorator.

        Returns:
            list: Each entry for the given column.

        Raises:
            ReadError: If reading data for the column fails.

        Example:
            
            ```
                for entry in read_column:
                    print(entry.username)
            ```

        """
        if session is None:
            raise DbEngineError("No session provided for read_column")

        try:
            with session:
                statement: SelectOfScalar[Any] = select(getattr(self.db_schema, column))
                all_entries: Sequence[SQLModel] = session.exec(statement).all()
                return all_entries
        except Exception as e:
            raise DbReadError(f'Reading column: "{column}" failed') from e

    @with_db_session
    def select_where(
        self, column: str, value: str, session: Optional[Session] = None
    ) -> SQLModel:
        """Select row for value found in column.

        Args:
            column (str): The column name to filter the row.
            value (str): The value to match in the specified column.
            session (Optional[Session], optional): 
                Defaults to use with decorator.

        Returns:
            Selected row as tuple.

        Raises:
            ReadError: If selecting data from the database fails.

        Example:
                
            ```
                row = select_where("username", "dummy_user")
                print(row)
            ```

        """
        if not session:
            raise DbEngineError("No session provided for select_where")

        try:
            with session:
                statement: SelectOfScalar[SQLModel] = select(self.db_schema).where(
                    getattr(self.db_schema, column) == value
                )
                results: ScalarResult[SQLModel] = session.exec(statement)
                row: SQLModel = results.one()

                self.logger.debug("Selected row where %s matches %s", column, value)
                return row
        except Exception as e:
            self._log_exception(e)
            raise DbReadError(
                f'Selecting column: "{column}" and value: "{value}" failed'
            ) from e

    @with_db_session
    def update_where(
        self, column: str, value: str, new_value: str, session: Optional[Session] = None
    ) -> bool:
        """Update row for value found in column.

        Args:
            column (str): The column name to filter the row.
            value (str): The value to match in the specified column.
            new_value (str): The new value to replace the old value.
            session (Optional[Session], optional): 
                Defaults to use with decorator.

        Returns:
            bool: True if update was successful, False otherwise.

        Raises:
            UpdateError: If updating data in the database fails.
        
        Example:
                
            ```
                update_where("username", "dummy_user", "new_dummy_user")
            ```

        """
        if not session:
            raise DbEngineError("No session provided for update_where")

        try:
            with session:
                statement: SelectOfScalar[SQLModel] = select(self.db_schema).where(
                    getattr(self.db_schema, column) == value
                )
                results: ScalarResult[SQLModel] = session.exec(statement)
                row: SQLModel = results.one()

                setattr(row, column, new_value)
                session.add(row)
                session.commit()

                self.logger.debug(
                    "Updated %s from: %s to: %s", column, value, new_value
                )
            return True
        except Exception as e:
            self._log_exception(e)
            raise DbUpdateError(
                f'In column: "{column}" select value: "{value}" update with: "{new_value}" failed'
            ) from e

    @with_db_session
    def delete_where(
        self, column: str, value: str, session: Optional[Session] = None
    ) -> None:
        """Delete row for value found in column.

        Args:
            column (str): The column name to filter the row.
            value (str): The value to match in the specified column.
            session (Optional[Session], optional): 
                Defaults to use with decorator.
        
        Returns:
            None

        Raises:
            DeleteError: If deleting data from the database fails.

        Example:
                    
             ```
                 delete_where("username", "dummy_user")
             ```
             
        """
        if not session:
            raise DbEngineError("No session provided for delete_where")

        try:
            with session:
                statement: SelectOfScalar[SQLModel] = select(self.db_schema).where(
                    getattr(self.db_schema, column) == value
                )
                results: ScalarResult[SQLModel] = session.exec(statement)
                row: SQLModel = results.one()

                session.delete(row)
                session.commit()

                self.logger.debug("Deleted row where %s matches %s", column, value)
        except Exception as e:
            self._log_exception(e)
            raise DbDeleteError(f'Deleting row for "{column}": "{value}" failed') from e


############ Debugging ############


# #Create 2 dummy users
def create_users():
    from db.models import AuthModel

    conn = SmitDb(AuthModel)
    user1: dict[str, str] = {
        "username": "dummy_user",
        "password": "$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om",
        "email": "dummy@dummymail.com",
        "sng_username": "dummy_sng_login",
        "sng_password": "dummy_sng_password",
        "daymeter": "199996",
        "nightmeter": "199997",
    }
    user2: dict[str, str] = {
        "username": "dummy_user2",
        "password": "$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om",
        "email": "dummy2@dummymail.com",
        "sng_username": "dummy2_sng_login",
        "sng_password": "dummy2_sng_password",
        "daymeter": "199994",
        "nightmeter": "199995",
    }
    users: dict[str, dict[str, str]] = {"dummy_user": user1, "dummy_user2": user2}

    instance1 = conn.db_schema.model_validate(user1)
    instance2 = conn.db_schema.model_validate(user2)

    conn.create_instance(instance1)
    conn.create_instance(instance2)


def read_users():
    from db.models import AuthModel

    conn = SmitDb(AuthModel)
    try:
        column_list = conn.read_column("username")

        print(column_list)
        print("try end")
    except Exception as exc:
        print(exc)
        print("except end")


#create_users()
#read_users()

# # # Print the dictionary
# # print(f"values: {users.values()}")
# # print(f"dict: {users.__dir__}")
# # print(f"keys: {users.keys()}")
# print(f"items: {users.items()}")
