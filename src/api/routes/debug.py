from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from sqlalchemy.engine.result import ScalarResult
from sqlmodel.sql.expression import SelectOfScalar

from pydantic import ValidationError

from utils.logger import Logger
from db.connection import get_db
from api import schemas, api_exceptions as exc

from api.opt.users_mock import valid_users, invalid_users

router = APIRouter()


@router.get("/dummyuser", response_model=schemas.UserResponseSchema)
async def get_user(
    db: Session = Depends(get_db),
) -> Any:
    """Return 'dummy_user' from the database.
    """
    try:
        statement: SelectOfScalar[schemas.UserModel] = select(schemas.UserModel).where(
            schemas.UserModel.username == "dummy_user"
        )
        user: schemas.UserModel = db.exec(statement).one()
        return user

    except Exception as e:
        raise e
    
@router.get('/users/')
async def get_users(
    db: Session = Depends(get_db),
) -> list[str]:
    """Get list of usernames."""

    existing_users: ScalarResult[schemas.UserModel] = db.exec(select(schemas.UserModel))

    usernames: List[str] = []
    for each in existing_users:
        usernames.append(each.username)
    return usernames

@router.get('/setup/users')
async def create_test_users(
    db: Session = Depends(get_db),
) -> str:
    """Create users from dependencies users dict."""

    existing_users: List[str] = await get_users(db)

    new_users: List[dict[str, str]] = valid_users()
    added_users: List[str] = []
    for usr in new_users:
        if usr['username'] not in existing_users:
            try:
                user: schemas.UserModel = schemas.UserModel.model_validate(usr)
            except ValidationError as ve:
                Logger().log_exception(ve)
                raise HTTPException(
                    status_code=400, detail=exc.ApiValidationError(ve).message()
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
                raise HTTPException(
                    status_code=500, detail=exc.DbSessionError(e).message()
                )
            
            added_users.append(user.username)
            Logger().logger.debug(f'Added user: {user.username}')

    if len(added_users) > 0:
        return f'Added users: {added_users}'
    else:
        return 'No new users added.'
