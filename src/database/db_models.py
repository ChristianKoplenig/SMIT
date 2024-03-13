from typing import Annotated, Optional, Any
from datetime import datetime
from sqlmodel import Field
from pydantic import ConfigDict

from schemas.user_schemas import UserBase

class UserModel(UserBase, table=True):
    """Table model for user entry in database.
    
    Connect to the user table in the database.
    Inherits from UserBase class.

    Columns:
        - id (Optional[int]): The ID of the user.
        - created_on (Optional[datetime]): The creation date of the user.
        - username (Mandatory[str]): The username of the user.
        - password (Mandatory[str]): The password of the user.
        - email (Optional[str]): The email address of the user.
        - sng_username (Optional[str]): The username for the SNG login.
        - sng_password (Optional[str]): The password for the SNG login.
        - daymeter (Optional[int]): The daymeter value of the user.
        - nightmeter (Optional[int]): The nightmeter value of the user.
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
                    "password": "$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6",
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

########################################################################

### Table for user configuration handling ###

# class ConfigSchema(SQLModel, table=True):
#     """
#     Represents the authentication configuration schema.

#     Attributes:
#         id (Optional[int]): The ID of the configuration.
#         created_on (Optional[datetime]): The creation date of the configuration.
#         preauth_mails (Optional[list]): The list of preauthorized email addresses.

#     Methods:
#         validate_preauth(cls, v: str, info: ValidationInfo) -> str:
#             Validates the email addresses for .

#     """

#     __tablename__: Any = "auth_config"

#     id: Annotated[Optional[int], Field(default=None, primary_key=True)]
#     created_on: Annotated[
#         Optional[datetime],
#         Field(default_factory=datetime.now, description="User creation date"),
#     ]

#     preauth_mails: Annotated[
#         Optional[str],
#         StringConstraints(
#             pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
#         ),
#         Field(
#             default=None,
#             description="Mail address for identification of preauthorized users",
#         ),
#     ]

#     # Needed for Column(JSON)
#     # Config: ConfigDict = {
#     #     'arbitrary_types_allowed' : True
#     # }

#     @field_validator("preauth_mails")
#     @classmethod
#     def validate_preauth(cls, v: str, info: ValidationInfo) -> str:
#         pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
#         if not re.match(pattern, v):
#             raise ValueError(f"{info.field_name} must be a valid email address")
#         return v