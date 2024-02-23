from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import ValidationError

from sqlalchemy.exc import NoResultFound

from db.connection import get_db
from api.schemas import UserModel
from api.api_exceptions import ApiValidationError
from utils.logger import Logger

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"authentication": "Not found"}},
)

@router.get("/user/{username}")
async def get_user(
    username: str,
    db: Session = Depends(get_db),
):
    """Return validated user row from the database."""
    try:
        statement = select(UserModel).where(
            UserModel.username == username
        )
        user = db.exec(statement).one()
        return user
    
    except ValidationError as ve:
        Logger().log_exception(ve)
        raise HTTPException(
            status_code=400,
            detail=ApiValidationError(ve).message()
        )
    
    except NoResultFound as nrf:
        return {"detail": f"User '{username}' not found."}

    except Exception as e:
        raise e
