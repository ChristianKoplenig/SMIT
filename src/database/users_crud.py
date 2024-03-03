"""Helper functions for user CRUD operations."""
from typing import Annotated, List
from sqlmodel import Session, select

from sqlalchemy.engine.result import ScalarResult
from sqlmodel.sql.expression import SelectOfScalar

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from pydantic import ValidationError
from exceptions.api_exc import ApiValidationError

from utils.logger import Logger
from database.db_models import UserModel

from schemas.user_schemas import UserResponseSchema
from schemas.response_schemas import (
    Response400,
    Response404,
    Response422,
    Response500,
)

class Users:
    """Class for user CRUD operations."""

    def __init__(self):
        Logger().log_module_init()

    async def create_user(
        self,
        user: Annotated[UserModel, "Schema for creating a user"],
        db: Annotated[Session, "Database session dependency"],
    ) -> UserModel:
        """create validated user"""
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            Logger().logger.info(
                f"Created user: {user.username} on table: {user.__tablename__}"
            )
            return user

        except ValidationError as ve:
            response422: Response422 = Response422(
                error="User input validation error",
                info=ApiValidationError(ve).message(),
            )
            raise HTTPException(
                status_code=422, detail=response422.model_dump()
            ) from ve

        except IntegrityError as ie:
            response400: Response400 = Response400(
                error="Unique constraint violation",
                info="Username already exists in database",
            )
            Logger().log_exception(ie)
            raise HTTPException(
                status_code=400, detail=response400.model_dump()
            ) from ie
        except Exception as e:
            Logger().log_exception(e)
            raise e

    async def get_user(
        self,
        username: Annotated[str, "Username to retrieve"],
        db: Annotated[Session, "Database session"],
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
            user: UserModel = db.exec(statement).one()

            return_model: UserResponseSchema = UserResponseSchema.model_validate(user)
            Logger().logger.info(
                f"Return user: {return_model.username} from table: {UserModel.__tablename__}"
            )
            return return_model

        except ValidationError as ve:
            response500: Response500 = Response500(
                error="Database Validation Error", info=ApiValidationError(ve).message()
            )
            Logger().log_exception(ve)
            raise HTTPException(
                status_code=500, detail=response500.model_dump()
            ) from ve

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
        db: Annotated[Session, "Database session"],
    ) -> list[str]:
        """Get list of registered usernames.

        Args:
            db (Session): The database session.

        Returns:
            list[str]: A list of registered usernames.
        """

        existing_users: ScalarResult[UserModel] = db.exec(select(UserModel))

        usernames: List[str] = []
        for each in existing_users:
            usernames.append(each.username)
        return usernames
