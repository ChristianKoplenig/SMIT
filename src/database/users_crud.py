"""Helper functions for user CRUD operations."""
from typing import Annotated, List
from sqlmodel import Session, select

from sqlalchemy.engine.result import ScalarResult
from sqlmodel.sql.expression import SelectOfScalar

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from pydantic import ValidationError
from exceptions.api_exc import ApiValidationError
from exceptions.db_exc import DatabaseError

from utils.logger import Logger
from database.db_models import UserModel

from schemas.user_schemas import UserResponseSchema
from schemas.response_schemas import (
    Response400,
    Response404,
    Response422,
    #Response500,
)

class Users:
    """Class for user CRUD operations."""

    def __init__(self):
        Logger().log_module_init()

    async def create_user(
        self,
        user: Annotated[UserModel, "Schema for creating a user"],
        session: Annotated[Session, "Database session dependency"],
    ) -> UserModel:
        """create validated user"""
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            Logger().logger.info(
                f"Created user: {user.username} on table: {user.__tablename__}"
            )
            return user
        
        except Exception as e:
            Logger().log_exception(e)
            session.rollback()
            raise DatabaseError(e, 'create user error')




    async def get_user(
        self,
        username: Annotated[str, "Username to retrieve"],
        session: Annotated[Session, "Database session"],
    ) -> UserResponseSchema:
        """Get user by username.

        Args:
            username (str): The username of the user to retrieve.
            db (Session): The database session.

        Returns:
            UserResponseSchema: The user response schema.

        Raises:
            Response404: If the user is not found.
            Response500: If there is a database validation error.
            Exception: Unexpected database error.
        """
        try:
            statement: SelectOfScalar[UserModel] = select(UserModel).where(
                UserModel.username == username
            )
            user: UserModel = session.exec(statement).one()

            return_model: UserResponseSchema = UserResponseSchema.model_validate(user)
            Logger().logger.info(
                f"Return user: {return_model.username} from table: {UserModel.__tablename__}"
            )
            return return_model

        # except ValidationError as ve:
        #     response500: Response500 = Response500(
        #         error="Database Validation Error", info=ApiValidationError(ve).message()
        #     )
        #     Logger().log_exception(ve)
        #     raise HTTPException(
        #         status_code=500, detail=response500.model_dump()
        #     ) from ve

        except NoResultFound as nrf:
            response404: Response404 = Response404(
                error="User not found", info=f"User '{username}' not in database."
            )
            Logger().log_exception(nrf)
            raise HTTPException(
                status_code=404, detail=response404.model_dump()
            ) from nrf

        except Exception as e:
            Logger().log_exception(e)
            raise e

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
