from typing import Annotated, Any
from fastapi import APIRouter, Depends
from sqlmodel import Session, SQLModel, select
from pydantic import StringConstraints

import db.models as models
from db.connection import get_db
from api import schemas

router = APIRouter()

class AllUsernames(SQLModel):
    """Validation schema for username list.

    Attributes:
        username (str): Validated username.
    """

    username: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            pattern=r"^[A-Za-z0-9_]+$",
            min_length=5,
        ),
    ]

@router.get("/user",
            response_model=schemas.UserBaseSchema
            )
async def get_user(
    #user: models.AuthModel,
    db: Session = Depends(get_db),
) -> Any:#schemas.UserBaseSchema:
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
        statement = select(
            models.AuthModel).where(
                models.AuthModel.username == "dummy_user")
        user: models.AuthModel = db.exec(statement).one()
        #response = models.AuthModel.model_dump_json(user)
    except Exception as e:
        raise e

    return user #response
    #return schemas.UserBaseSchema.model_validate(response)  # response
    #return db.exec(statement).one()