import os
from dotenv import load_dotenv
from datetime import timedelta
from typing import Annotated, Any
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from database.connection import get_db
from schemas.response_schemas import Response401, Response404, Response500
from schemas.auth_schemas import AuthToken
from schemas.user_schemas import UserResponseSchema, LoginFormOutput

from api.components.authenticate import (get_user,
                                 authenticate_user,
                                 create_access_token,
                                 get_current_user,
                                 )

from database.users_crud import get_userlist

# Load secrets
load_dotenv()
token_expire: str | None = os.getenv('SMIT_TOKEN_ACCESS_TOKEN_EXPIRE_MINUTES')
if token_expire:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(token_expire)
else:
    ACCESS_TOKEN_EXPIRE_MINUTES = 0


router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        401: {"model": Response401},
        404: {"model": Response404},
        500: {"model": Response500},
    },
)

@router.get("/user/test")
async def get_dummy_user(
    db: Session = Depends(get_db),
    ) -> UserResponseSchema:
    """Test route to get a hardcoded dummy user.
    
    Returns:
        UserResponseSchema: Dummy user row.
    """
    name = "dummy_user"
    dummy: UserResponseSchema = await get_user(name, db=db)
    return dummy

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
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
    user: UserResponseSchema = await authenticate_user(form_data.username,
                                                       form_data.password,
                                                       db=db)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    sub_data = f'auth:{user.username}'
    access_token: str = create_access_token(
        data={"sub": sub_data},
        expires_delta=access_token_expires
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

@router.get(
    "/user/{username}",
    response_model=UserResponseSchema,
    )
async def get_user_by_path(
    username: str,
    db: Session = Depends(get_db)
    ) -> UserResponseSchema:
    """Path operation to get user by username.

    Args:
        username (str): The username of the user to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        UserResponseSchema: User data row from database.
    """
    user: UserResponseSchema = await get_user(username, db=db)
    return user

################################

@router.post("/login")
async def login_form(
    #form_data: Annotated[LoginFormInput, 'Name, Password'],
    #login_data: Annotated[LoginFormInput, 'Login input data'],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],


    db: Session = Depends(get_db),
    #auth = Annotated[str, Depends(authenticate_user)],
    #token = Depends(oauth2_scheme),
): # -> bool:
    """get username password

    Returns:
        bool: true on sucessful login
    """
    db_users: list[str] = await get_userlist(db=db)

    try:
        user = await authenticate_user(username, password, db)
        user.logged_in = True
        logged_in = LoginFormOutput.model_validate(user)
        return logged_in
    except Exception as e:
        raise e
    #username = auth

    # if username not in db_users:
    #     return False
    #return False #login_data
