"""Router for user operations."""
import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from api.dependencies import dep_session

from database.db_models import UserModel
from database.db_users import Users

from schemas.user_schemas import UserInputSchema, UserResponseSchema
from schemas.response_schemas import DatabaseErrorResponse

from exceptions.db_exc import DatabaseError

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
        500: {"model": DatabaseErrorResponse},
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
        new_user: UserModel = await Users().create_user(db_user, session=session)
        response_user: UserResponseSchema = UserResponseSchema.model_validate(new_user)
        return response_user
    
    except DatabaseError as dbe:
        raise HTTPException(
            status_code=500, 
            detail=dbe.http_message())

    except Exception as e:
        raise e
