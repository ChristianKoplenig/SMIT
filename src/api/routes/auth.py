from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from sqlmodel.sql.expression import SelectOfScalar
from jose import JWTError, jwt

from pydantic import ValidationError
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.exc import NoResultFound

from db.connection import get_db
from utils.logger import Logger
from utils.hasher import Hasher
from api.api_exceptions import ApiValidationError
from api.response_schemas import Response401, Response404, Response500
from api.schemas import (
    AuthToken,
    TokenData,
    UserModel,
    UserResponseSchema,
)

# Token settings
SECRET_KEY = "0a9aaaa7137fb23dca13411fd3593bbc3ca3095be37d0e70883fd9e979dba19e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Router setup
router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        401: {"model": Response401},
        404: {"model": Response404},
        500: {"model": Response500},
    },
)

# Scheme for OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# Logic
async def get_user(
    username: str,
    db: Session,
) -> UserResponseSchema:
    """Get user by username."""
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
    """Get list of registered usernames."""

    existing_users: ScalarResult[UserModel] = db.exec(select(UserModel))

    usernames: List[str] = []
    for each in existing_users:
        usernames.append(each.username)
    return usernames


async def authenticate_user(username: str,
                            password: str,
                            db: Session = Depends(get_db),
    ) -> UserResponseSchema:
    try:
        user: UserResponseSchema = await get_user(username, db=db)

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
        
    except Exception as e:
        Logger().log_exception(e)
        raise e

    if not Hasher().verify_password(password, user.password):
        error_detail = Response401(
            info=f"Pasword for user '{username}' does not match.",
        )
        raise HTTPException(
            status_code=401,
            detail=error_detail.model_dump(),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_access_token(data: dict,
                        expires_delta: timedelta | None = None
                        ) -> str:
    to_encode: dict[Any, Any] = data.copy()

    if expires_delta:
        expire: datetime = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
    ) -> UserResponseSchema:

    credentials_error = Response401(info="Could not validate credentials")

    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail=credentials_error.model_dump(),
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username)
    except JWTError as e:
        Logger().log_exception(e)
        raise e

    if token_data.username:
        user: UserResponseSchema = await get_user(token_data.username, db=db)
        return user
    else:
        raise HTTPException(
            status_code=401,
            detail=credentials_error.model_dump(),
            headers={"WWW-Authenticate": "Bearer"},
        )


# Path operations
@router.get("/user/test")
async def get_dummy_user(
    db: Session = Depends(get_db),
    ) -> UserResponseSchema:
    name = "dummy_user"
    dummy: UserResponseSchema = await get_user(name, db=db)
    return dummy


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
    ) -> AuthToken:
    """Login route for token generation."""
    user: UserResponseSchema = await authenticate_user(form_data.username,
                                                       form_data.password,
                                                       db=db)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: str = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return AuthToken(access_token=access_token, token_type="bearer")


@router.get("/user/me")
async def read_user_me(
    current_user: Annotated[UserResponseSchema, Depends(get_current_user)],
    ) -> UserResponseSchema:
    """Return the logged in username."""
    return current_user


@router.get(
    "/user/{username}",
    response_model=UserResponseSchema,
    )
async def get_user_by_path(
    username: str,
    db: Session = Depends(get_db)
    ) -> UserResponseSchema:
    """Path operation to get user by username."""
    user: UserResponseSchema = await get_user(username, db=db)
    return user
