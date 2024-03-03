from typing import Any, Callable, Generator, List

from database.connection import Db
from database.db_models import UserModel
from database.users_crud import Users
from exceptions.api_exc import ApiValidationError, DbSessionError
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from schemas.user_schemas import UserResponseSchema
from sqlalchemy.engine.result import ScalarResult
from sqlmodel import Session, select
from sqlmodel.sql.expression import SelectOfScalar
from utils.logger import Logger
from utils.users_mock import valid_users

# Dependencies
dep_get_db: Callable[[], Generator[Session, Any, None]] = Db().get_db

router = APIRouter()


@router.get("/dummyuser")
async def get_dummy_user(
    session: Session = Depends(dep_get_db),
) -> UserResponseSchema:
    """Return 'dummy_user', bypass UserCrud class."""
    try:
        statement: SelectOfScalar[UserModel] = select(UserModel).where(
            UserModel.username == "dummy_user"
        )
        user: UserModel = session.exec(statement).one()
        dummy_user: UserResponseSchema = UserResponseSchema.model_validate(user)
        return dummy_user

    except Exception as e:
        raise e


@router.get("/userslist/")
async def get_userslist(
    db: Session = Depends(dep_get_db),
) -> list[str]:
    """Get all usernames, bypass UserCrud class."""

    existing_users: ScalarResult[UserModel] = db.exec(select(UserModel))

    usernames: List[str] = []
    for each in existing_users:
        usernames.append(each.username)
    return usernames


@router.get(
    "/user/{username}",
    response_model=UserResponseSchema,
)
async def get_user_by_path(
    username: str,
    db: Session = Depends(dep_get_db),
) -> UserResponseSchema:
    """Path operation to get user by username.

    Args:
        username (str): The username of the user to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        UserResponseSchema: User data row from database.
    """
    user: UserResponseSchema = await Users().get_user(username, db=db)
    return user


@router.get("/setup/dummyusers")
async def create_dummy_users(
    db: Session = Depends(dep_get_db),
) -> str:
    """Use valid user dict from `utils.users_mock` file to create users."""

    existing_users: List[str] = await get_userslist(db)

    new_users: List[dict[str, str]] = valid_users()
    added_users: List[str] = []
    for usr in new_users:
        if usr["username"] not in existing_users:
            try:
                user: UserModel = UserModel.model_validate(usr)
            except ValidationError as ve:
                Logger().log_exception(ve)
                raise HTTPException(
                    status_code=400, detail=ApiValidationError(ve).message()
                )
            except Exception as e:
                Logger().log_exception(e)
                raise e

            try:
                db.add(user)
                db.commit()
                db.refresh(user)
            except Exception as e:
                Logger().log_exception(e)
                raise HTTPException(status_code=500, detail=DbSessionError(e).message())

            added_users.append(user.username)
            Logger().logger.debug(f"Added user: {user.username}")

    if len(added_users) > 0:
        return f"Added users: {added_users}"
    else:
        return "No new users added."
