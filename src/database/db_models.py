"""Table models for database connections."""
from typing import Annotated, Optional, Any
from datetime import datetime
from sqlmodel import Field
from pydantic import ConfigDict

from schemas.user_schemas import UserBase

class UserModel(UserBase, table=True):
    """Table model for database connection.

    Create id, and created_on fields on database commit.
    """

    __tablename__: Any = "auth_api"

    id: Annotated[Optional[int], Field(default=None, primary_key=True)]
    created_on: Annotated[
        Optional[datetime],
        Field(default_factory=datetime.now, description="User creation date"),
    ]

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "dummy_user",
                    "password": "$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om",
                    "email": "dummy@dummymail.com",
                    "sng_username": "dummy_sng_login",
                    "sng_password": "dummy_sng_password",
                    "daymeter": 199996,
                    "nightmeter": 199997,
                    "id": 1,
                    "created_on": "2023-09-25T10:15:00",
                }
            ]
        }
    }