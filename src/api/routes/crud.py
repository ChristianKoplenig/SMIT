"""Router for CRUD operations."""
import os
from typing import Annotated, Any, Callable, Generator

from database.connection import Db
from database.db_models import UserModel
from database.users_crud import Users
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from schemas.response_schemas import (
    Response400,
    Response401,
    Response404,
    Response422,
    Response500,
)
from schemas.user_schemas import UserInputSchema, UserResponseSchema
from sqlmodel import Session

# Load secrets
load_dotenv()
token_expire: str | None = os.getenv("SMIT_TOKEN_ACCESS_TOKEN_EXPIRE_MINUTES")
if token_expire:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(token_expire)
else:
    ACCESS_TOKEN_EXPIRE_MINUTES = 0

# Dependencies
dep_get_db: Callable[[], Generator[Session, Any, None]] = Db().get_db

router: APIRouter = APIRouter(
    prefix="/crud",
    tags=["CRUD Operations"],
    responses={
        400: {"model": Response400},
        # 401: {"model": Response401},
        # 404: {"model": Response404},
        422: {"model": Response422},
        500: {"model": Response500},
    },
)


@router.post("/user/create")
async def create_new_user(
    user: Annotated[UserInputSchema, "Schema for user creation."],
    db: Session = Depends(dep_get_db),
) -> UserResponseSchema:
    """Create a new user.

    Depends:
        get_db: The database session.

    Args:
        user (UserInputSchema): The user input schema.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        Response400: If the user already exists in database.
        Response422: If the user input is invalid.
        Exception: On unexpected database error.

    """
    try:
        db_user: UserModel = UserModel.model_validate(user)
        new_user: UserModel = await Users().create_user(db_user, db)
        response_user: UserResponseSchema = UserResponseSchema.model_validate(new_user)
        return response_user

    except Exception as e:
        raise e
