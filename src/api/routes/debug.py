from typing import Any
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from db.connection import get_db

from sqlmodel.sql.expression import SelectOfScalar

from api import schemas

router = APIRouter()


@router.get("/user", response_model=schemas.UserResponseSchema)
async def get_user(
    db: Session = Depends(get_db),
) -> Any: #schemas.UserResponseSchema:
    """
    Return a list of all usernames.

    This function retrieves all usernames from the database and returns them as a list.
    If there is a database validation error, a 404 status code will be raised.

    Parameters:
    - session: The database session to use for the query.

    Returns:
    - A list of usernames.

    Raises:
    - HTTPException: 404 - On database validation error.

    """
    try:
        statement: SelectOfScalar[schemas.UserModel] = select(schemas.UserModel).where(
            schemas.UserModel.username == "dummy_user"
        )
        user: schemas.UserModel = db.exec(statement).one()
        return user

    except Exception as e:
        raise e
    

