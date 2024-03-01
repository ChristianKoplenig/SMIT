"""Helper functions for user CRUD operations."""
from typing import List
from sqlmodel import Session, select
from sqlmodel.sql.expression import SelectOfScalar
from fastapi import Depends, HTTPException
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.exc import NoResultFound
from pydantic import ValidationError

from database.connection import get_db
from database.db_models import UserModel

from utils.logger import Logger

from schemas.user_schemas import UserResponseSchema, CreateUserInput
from schemas.response_schemas import Response404, Response500
from exceptions.api_exc import ApiValidationError



async def get_user(
    username: str,
    db: Session,
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
        raise HTTPException(status_code=500, detail=response500.model_dump()) from ve

    except NoResultFound as nrf:
        response404: Response404 = Response404(
            error="User not found", info=f"User '{username}' not in database."
        )
        Logger().log_exception(nrf)
        raise HTTPException(status_code=404, detail=response404.model_dump()) from nrf

    except Exception as e:
        Logger().log_exception(e)
        raise e


async def get_userlist(
    db: Session = Depends(get_db),
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


#############################################
# Create User
# async def create_user(
#         user: Annotated[CreateUserInput, 'Schema for creating a user'],
#         db: Annotated[Session, Depends(get_db)],
# ):
#     """create validated user"""
#     try:
#         db.add(user)
#         db.commit()
#         db.refresh(user)
#         return user
#     except ValidationError as ve:
#         response: Response404 = Response404(
#             error='User input validation error',
#             info=ApiValidationError(ve).message()
#         )


# Delete User