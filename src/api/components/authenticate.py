"""Helper functions for authenticating users."""
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from api.dependencies import dep_session
from database.crud import Crud
from database.db_models import UserModel
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from schemas.auth_schemas import TokenData
from schemas.response_schemas import Response401
from schemas.user_schemas import UserResponseSchema
from sqlmodel import Session
from utils.hasher import Hasher
from utils.logger import Logger

# Import secrets
load_dotenv()
ALGORITHM: str | Any = os.getenv("SMIT_TOKEN_ALGORITHM")
SECRET_KEY: str | Any = os.getenv("SMIT_TOKEN_SECRET_KEY")


# Scheme for OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def authenticate_user(
    username: str,
    password: str,
    session: Annotated[Session, Depends(dep_session)],
) -> UserResponseSchema:
    """Get user and verify password.

    Args:
        username (str): Username for authentication.
        password (str): The password of the user.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        UserResponseSchema: User row entry from database.

    Raises:
        Response401: Unknown user / password does not match.
        Exception: General database exception.
    """
    try:
        user: UserResponseSchema = await Crud().get(
            datamodel=UserModel,
            column="username",
            value=username,
            returnmodel=UserResponseSchema,
            session=session)

    except HTTPException as hte:
        if hte.status_code == 404:
            error_detail = Response401(
                info=f"User '{username}' not registered.",
            )
            raise HTTPException(
                status_code=401,
                detail=error_detail.model_dump(),
                headers={"WWW-Authenticate": "Bearer"},
            ) from hte
        else:
            raise hte

    except Exception as e:
        Logger().log_exception(e)
        raise e

    # Verify password
    password_verified: bool = Hasher().verify_password(password, user.password)
    if not password_verified:
        error_detail = Response401(
            info=f"Pasword for user '{username}' does not match.",
        )
        raise HTTPException(
            status_code=401,
            detail=error_detail.model_dump(),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Use jwt library to create an access token.

    Args:
        data (dict): The data to be encoded in the token.
        expires_delta (timedelta | None, optional):
            The expiration time delta for the token. Defaults to None.

    Returns:
        str: The encoded access token.
    """

    to_encode: dict[Any, Any] = data.copy()

    if expires_delta:
        expire: datetime = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(dep_session)],
) -> UserResponseSchema:
    """Retrieves user based on provided token.

    Args:
        token (str): The authentication token.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        UserResponseSchema: User row entry from database.

    Raises:
        Response401: If token data is invalid.
        JWTError: If token decoding/handling fails.
    """
    credentials_error = Response401(info="Could not validate credentials")

    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub_data: str | None = payload.get("sub")

        if sub_data:
            username: str = sub_data.split(":")[1]

        if sub_data is None:
            raise HTTPException(
                status_code=401,
                detail=credentials_error.model_dump(),
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username)

    except ExpiredSignatureError as ese:
        exp_error = Response401(info="Token has expired")
        raise HTTPException(
            status_code=401,
            detail=exp_error.model_dump(),
            headers={"WWW-Authenticate": "Bearer"},
        ) from ese

    except JWTError as e:
        Logger().log_exception(e)
        raise e

    if token_data.username:
        user: UserResponseSchema = await Crud().get(
            value=token_data.username,
            datamodel=UserModel,
            column="username",
            returnmodel=UserResponseSchema,
            session=session)
        Logger().logger.debug(f"User: {username} logged in using token")
        return user
    else:
        raise HTTPException(
            status_code=401,
            detail=credentials_error.model_dump(),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: Annotated[UserResponseSchema, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
