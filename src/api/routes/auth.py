from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import ValidationError

from sqlmodel.sql.expression import SelectOfScalar
from sqlalchemy.exc import NoResultFound

from db.connection import get_db
from api.api_exceptions import ApiValidationError
from utils.logger import Logger
from api.schemas import (UserModel,
                         UserResponseSchema,
                         Response404,
                         Response500
                         )

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        404: {"model": Response404},
        500: {"model": Response500},
    }
)

@router.get("/user/{username}",
            response_model=UserResponseSchema,
            )
async def get_user(
    username: str,
    db: Session = Depends(get_db),
) -> UserResponseSchema:
    """Return validated user row from the database."""
    try:
        statement: SelectOfScalar[UserModel] = select(UserModel).where(
            UserModel.username == username
        )
        user: UserModel = db.exec(statement).one()

        return_model: UserResponseSchema = UserResponseSchema.model_validate(user)
        return return_model
    
    except ValidationError as ve:
        response500: Response500 = Response500(
            error="Database Validation Error", 
            info=ApiValidationError(ve).message()
        )
        Logger().log_exception(ve)
        raise HTTPException(
            status_code=500,
            detail=response500.model_dump()
        ) from ve
    
    except NoResultFound as nrf:
        response404 = Response404(
            error="User not found",
            info=f"User '{username}' not in database."
        )
        raise HTTPException(
            status_code=404,
            detail= response404.model_dump()
        ) from nrf

    except Exception as e:
        raise e
