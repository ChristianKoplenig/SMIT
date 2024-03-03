import os
from datetime import timedelta
from typing import Annotated, Any, Callable, Generator

from api.components.authenticate import (
    authenticate_user,
    create_access_token,
    get_current_user,
)
from database.connection import Db
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth_schemas import AuthToken
from schemas.response_schemas import Response401, Response404, Response500
from schemas.user_schemas import UserResponseSchema
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
    prefix="/auth",
    tags=["Authentication"],
    responses={
        401: {"model": Response401},
        404: {"model": Response404},
        500: {"model": Response500},
    },
)


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(dep_get_db),
) -> AuthToken:
    """Login route for token generation.

    Use form data to authenticate user.
    Generate access token and set expire timedelta.

    Args:
        form_data (OAuth2PasswordRequestForm):
            The form data containing the username and password.
        db (Session, optional):
            The database session. Defaults to Depends(get_db).

    Returns:
        AuthToken: The generated access token.
    """
    user: UserResponseSchema = await authenticate_user(
        form_data.username, form_data.password, db=db
    )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    sub_data: str = f"auth:{user.username}"
    access_token: str = create_access_token(
        data={"sub": sub_data}, expires_delta=access_token_expires
    )
    return AuthToken(access_token=access_token, token_type="bearer")


@router.get("/user/me")
async def read_user_me(
    current_user: Annotated[UserResponseSchema, Depends(get_current_user)],
) -> UserResponseSchema:
    """Use token to get user data for logged in user.

    Get the user data for the currently logged in user.
    Needs authentication token to be passed in the header.

    Depends:
        get_current_user: Use token to get user data.

    Parameters:
        current_user (UserResponseSchema):
            User data row from database.

    Returns:
        UserResponseSchema: User data row from database.
    """
    return current_user
