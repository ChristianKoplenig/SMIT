"""Helper functions for user CRUD operations."""
from typing import Annotated, List, Generator, Any, Type

from exceptions.api_exc import ApiValidationError
from exceptions.db_exc import DatabaseError
from fastapi import HTTPException
from pydantic import ValidationError
from schemas.user_schemas import UserResponseSchema
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, select, SQLModel
from sqlmodel.sql.expression import SelectOfScalar
from utils.logger import Logger

from database.db_models import UserModel

# from schemas.response_schemas import (
#     Response400,
#     Response404,
#     Response422,
#     #Response500,
# )

class Crud:
    """Class for user CRUD operations."""

    def __init__(self):
        Logger().log_module_init()

    async def post(
        self,
        datamodel: Annotated[SQLModel, "Schema for creating a user"],
        session: Annotated[Session, "Database session dependency"],
    ) -> SQLModel:
        """Create model data on database
        
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
        returnmodel: Annotated[SQLModel, "ORM model schema for database table"],
        session: Annotated[Session, "Database session"],
    ) -> SQLModel:
        """Get user by username.

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

            db_row: SQLModel = returnmodel.model_validate(user)
            Logger().logger.info(
                f'Return user: "{db_row.username}" from table: "{datamodel.__tablename__}"'
            )
            return db_row

        # except ValidationError as ve:
        #     response500: Response500 = Response500(
        #         error="Database Validation Error", info=ApiValidationError(ve).message()
        #     )
        #     Logger().log_exception(ve)
        #     raise HTTPException(
        #         status_code=500, detail=response500.model_dump()
        #     ) from ve

        # except NoResultFound as nrf:
        #     response404: Response404 = Response404(
        #         error="User not found", info=f"User '{username}' not in database."
        #     )
        #     Logger().log_exception(nrf)
        #     raise HTTPException(
        #         status_code=404, detail=response404.model_dump()
        #     ) from nrf

        except Exception as e:
            Logger().log_exception(e)
            session.rollback()
            raise DatabaseError(e, "get from db error")

    async def get_userlist(
        self,
        session: Annotated[Session, "Database session"],
    ) -> list[str]:
        """Get list of registered usernames.

        Args:
            db (Session): The database session.

        Returns:
            list[str]: A list of registered usernames.
        """

        existing_users: ScalarResult[UserModel] = session.exec(select(UserModel))

        usernames: List[str] = []
        for each in existing_users:
            usernames.append(each.username)
        return usernames
