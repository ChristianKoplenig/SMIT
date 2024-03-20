from typing import Annotated, List, Type, TypeVar
from sqlmodel import Session, select, SQLModel
from sqlalchemy.engine.result import ScalarResult
from sqlmodel.sql.expression import SelectOfScalar

from exceptions.db_exc import DatabaseError
from utils.logger import Logger

# Annotate return values as instances of SQLModel class
ReturnType = TypeVar("ReturnType", bound=SQLModel)

class Crud:
    """SqlModel CRUD operations.
    
    Use SqlModel models and session to perform CRUD operations on database.

    Methods:
        post: Use SqlModel to create data entry.
        get: Select entry with column name and pattern.
        get_column_entries: Return list of all entries from column.
        put: Select database row and update entry.
        delete: Delete database row.
    """

    def __init__(self) -> None:
        Logger().log_module_init()

    async def post(
        self,
        datamodel: Annotated[SQLModel, "Schema for creating a user"],
        session: Annotated[Session, "Database session dependency"],
    ) -> SQLModel:
        """Use SqlModel to create data entry.
        
        Insert data into database table.
        Refresh the ORM model and return it.

        Args:
            datamodel (SqlModel): The data model to create at database.
            db (Session): The database session.
        
        Returns:
            SqlModel: Return the ORM input model.

        Raises:
            DatabaseError: If creation fails on database error.
        
        """
        try:
            session.add(datamodel)
            session.commit()
            session.refresh(datamodel)
            Logger().logger.info(
                f'Created data using ORM model: "{datamodel.__class__.__name__}" '
                f'on table: "{datamodel.__tablename__}"'
            )
            return datamodel
        
        except Exception as e:
            Logger().log_exception(e)
            session.rollback()
            raise DatabaseError(e, 'create on db error')

    async def get(
        self,
        datamodel: Annotated[Type[SQLModel], 'ORM model schema for database table'],
        column: Annotated[str, "Table column to search value in."],
        value: Annotated[str, "Match pattern to select row."],
        returnmodel: Annotated[Type[ReturnType], "ORM model schema for database table"],
        session: Annotated[Session, "Database session"],
    ) -> ReturnType:
        """Select entry with column name and pattern.

        Args:
            datamodel (SQLModel): Database table schema.
            column (str): The column to search for value.
            value (str): The value to search for in column.
            returnmodel (SQLModel): Schema for database response.
            session (Session): The database session.

        Returns:
            SQLModel: The model row retrieved from database.

        Raises:
            DatabaseError: If creation fails on database error.
        """
        try:
            statement: SelectOfScalar[SQLModel] = select(datamodel).where(
                getattr(datamodel, column) == value
            )

            user: SQLModel = session.exec(statement).one()

            db_row: ReturnType = returnmodel.model_validate(user)
            Logger().logger.info(
                f'Return user: "{db_row.username}" '
                f'from table: "{datamodel.__tablename__}"'
            )
            return db_row

        except Exception as e:
            Logger().log_exception(e)
            session.rollback()
            raise DatabaseError(e, "get from db error")

    async def get_column_entries(
        self,
        datamodel: Annotated[Type[SQLModel], "ORM model schema for database table"],
        column: Annotated[str, "Table column to search value in."],
        session: Annotated[Session, "Database session"],
    ) -> list[str]:
        """Return list of all entries from column.
        
        Args:
            datamodel (SQLModel): Database table schema.
            column (str): The column to search for value.
            session (Session): The database session.

        Returns:
            list[str]: List with column entries.

        Raises:
            DatabaseError: If getting values fails.
        """
        try:
            db_entries: ScalarResult[SQLModel] = session.exec(
                select(getattr(datamodel, column))
                )
            entries_list: List[str] = [str(each) for each in db_entries]
            return entries_list
        
        except Exception as e:
            Logger().log_exception(e)
            session.rollback()
            raise DatabaseError(e, "get_column_entries from db error")

    async def put(
        self,
        datamodel: Annotated[Type[SQLModel], 'ORM model schema for database table'],
        select_column: Annotated[str, "Table column to search select_value in."],
        select_value: Annotated[str, "Match pattern to select database entry."],
        update_entry: Annotated[str, "Database entry to update."],
        update_value: Annotated[str, "New value to update entry with."],
        returnmodel: Annotated[SQLModel, "ORM model schema for response"],
        session: Annotated[Session, "Database session"],
    ) -> SQLModel:
        """Select database row and update entry.
        
        Args:
            datamodel (SQLModel): Database table schema.
            select_column (str): The column to search for value.
            select_value (str): The value to search for in column.
            update_entry (str): The column to update.
            update_value (str): The new value to update entry with.
            returnmodel (SQLModel): Schema for database response.
            session (Session): The database session.

        Returns:
            SQLModel: The updated model row from database.

        Raises:
            DatabaseError: If update fails on database error.
        """
        try:
            statement: SelectOfScalar[SQLModel] = select(datamodel).where(
                getattr(datamodel, select_column) == select_value
            )
            on_db: SQLModel = session.exec(statement).one()

            # Update entry
            setattr(on_db, update_entry, update_value)
            
            # Validate entry; Raise error before commit
            updated_entry: SQLModel = returnmodel.model_validate(on_db)
            
            session.add(on_db)
            session.commit()
            session.refresh(on_db)
            Logger().logger.info(
                f'Updated entry for: "{update_entry}" to new value: "{update_value}" '
                f'on table: "{datamodel.__tablename__}"'
            )
            return updated_entry

        except Exception as e:
            Logger().log_exception(e)
            session.rollback()
            raise DatabaseError(e, "update on db error")

    async def delete(
        self,
        datamodel: Annotated[Type[SQLModel], 'ORM model schema for database table'],
        column: Annotated[str, "Table column to search value in."],
        value: Annotated[str, "Match pattern to select row for deletion."],
        session: Annotated[Session, "Database session"],
    ) -> str:
        """Delete database row.
        
        Args:
            datamodel (SQLModel): Database table schema.
            column (str): The column to search for value.
            value (str): The value to search for in column.
            session (Session): The database session.
        
        Returns:
            str: Message of deleted entry.

        Raises:
            DatabaseError: If delete fails on database error.
        """
        try:
            statement: SelectOfScalar[SQLModel] = select(datamodel).where(
                getattr(datamodel, column) == value
            )
            on_db: SQLModel = session.exec(statement).one()
            session.delete(on_db)
            session.commit()
            Logger().logger.info(
                f'Deleted entry: "{column} == {value}" '
                f'on table: "{datamodel.__tablename__}"'
            )
            return (
                f'Deleted entry: "{column} == {value}" '
                f'on table: "{datamodel.__tablename__}"'
            )

        except Exception as e:
            Logger().log_exception(e)
            session.rollback()
            raise DatabaseError(e, "delete from db error")
