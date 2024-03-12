"""Router for user operations."""
import os
from dotenv import load_dotenv
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, SQLModel

from api.dependencies import dep_session
from database.crud import Crud
from utils.logger import Logger

from database.db_models import UserModel
from exceptions.db_exc import DatabaseError
from schemas.response_schemas import DatabaseErrorResponse, DatabaseErrorSchema
from schemas.user_schemas import UserInputSchema, UserResponseSchema

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
        get_db: The database session.

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
