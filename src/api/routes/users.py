"""Router for user operations."""
import os
from dotenv import load_dotenv
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, SQLModel

from api.dependencies import dep_session
from api.components.authenticate import get_current_user
from database.crud import Crud
from utils.logger import Logger

from database.db_models import UserModel
from exceptions.db_exc import DatabaseError
from schemas.response_schemas import DatabaseErrorResponse, DatabaseErrorSchema
from schemas.user_schemas import UserInputSchema, UserResponseSchema, UserlistSchema, UserUpdateSchema

# Load secrets
load_dotenv()
token_expire: str | None = os.getenv("SMIT_TOKEN_ACCESS_TOKEN_EXPIRE_MINUTES")
if token_expire:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(token_expire)
else:
    ACCESS_TOKEN_EXPIRE_MINUTES = 0


router: APIRouter = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={
        500: {"model": DatabaseErrorSchema},
    },
)


@router.post("/user/create")
async def create_new_user(
    user: Annotated[UserInputSchema, "Schema for user creation."],
    session: Annotated[Session, Depends(dep_session)],
) -> UserResponseSchema:
    """Create a new user.

    Depends:
        dep_session: The database session.

    Args:
        user (UserInputSchema): The user input schema.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 500 - On database error.

    """
    try:
        db_user: UserModel = UserModel.model_validate(user)
        new_user: SQLModel = await Crud().post(db_user, session=session)
        response_user: UserResponseSchema = UserResponseSchema.model_validate(new_user)
        return response_user
    
    except DatabaseError as dbe:
        Logger().log_exception(dbe)
        raise DatabaseErrorResponse(dbe)

    except Exception as e:
        Logger().log_exception(e)
        raise e

@router.get('/allusers')
async def get_all_users(
    session: Annotated[Session, Depends(dep_session)],
) -> UserlistSchema:
    """Get list of all users.
    
    Depends:
        dep_session: The database session.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:    
        UserlistSchema: A list with all usernames.

    Raises: 
        HTTPException: 500 - On database error.
    """
    try:
        userlist: list[str] = await Crud().get_column_entries(
            datamodel=UserModel,
            column="username",
            session=session,
        )
        return UserlistSchema(userlist=userlist)

    except DatabaseError as dbe:
        Logger().log_exception(dbe)
        raise DatabaseErrorResponse(dbe)

    except Exception as e:
        Logger().log_exception(e)
        raise e


@router.get("/user/{username}")
async def get_user(
    username: str,
    session: Annotated[Session, Depends(dep_session)],
) -> UserResponseSchema:
    """Get user by username.

    Args:
        username (str): The username to search for.
        session (Session): The database session.

    Returns:
        UserResponseSchema: The user response schema.

    Raises:
        HTTPException: 404 - If user not found.
        HTTPException: 500 - On database error.
    """
    try:
        user: UserResponseSchema = await Crud().get(
            datamodel=UserModel,
            column="username",
            value=username,
            returnmodel=UserResponseSchema,
            session=session,
        )
        return user

    except DatabaseError as dbe:
        Logger().log_exception(dbe)
        raise DatabaseErrorResponse(dbe)

    except Exception as e:
        Logger().log_exception(e)
        raise e
    
@router.patch("/user/patch",
              response_model=UserResponseSchema)
async def update_user(
    current_user: Annotated[UserResponseSchema, Depends(get_current_user)],
    data: Annotated[UserUpdateSchema, 'User data for update.'],
    session: Annotated[Session, Depends(dep_session)],
) -> SQLModel:
    """Update user by id.
    
    Args:
        current_user (UserResponseSchema): Current logged in user.
        data (UserUpdateSchema): The user data for update.
        session (Session): The database session.

    Returns:
        UserResponseSchema: The updated user.

    Raises:
        DatabaseErrorResponse: On database error.
        Exception: On any other error.
    """
    db_user: UserResponseSchema = current_user

    try:
        updated_user: SQLModel = await Crud().patch(
            column='id',
            value=db_user.id,
            datamodel=UserModel,
            new_data=data,
            session=session)
        return updated_user

    except DatabaseError as dbe:
        Logger().log_exception(dbe)
        raise DatabaseErrorResponse(dbe)

    except Exception as e:
        Logger().log_exception(e)
        raise e
