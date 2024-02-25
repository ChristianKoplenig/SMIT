from datetime import datetime
from typing import Annotated, Optional, Any, Union
from sqlmodel import SQLModel, Field
from pydantic import StringConstraints, ConfigDict 
#from .schemas import ErrorResponses

# Needed for field validators
# import re
# from pydantic import ValidationInfo, field_validator

class UserBase(SQLModel):
    """Base model schema for user management.

    Validate all fields needed for user management.

    Attributes:
        - username (str): Authentication username; mandatory field for authenticator.
            - Strip whitespace
            - Convert to lowercase
            - Must consist of alphanumeric characters and underscores only
            - Minimum length of 5 characters
        - password (str): Authentication password; mandatory field for authenticator.
            - Must be a hash value
        - email (str, optional): The email address of the user.
            - Must be a valid email address
        - sng_username (str, optional): The username for energy provider login.
            - Must consist of alphanumeric characters and underscores only
        - sng_password (str, optional): The password for energy provider login.
        - daymeter (int, optional): The day meter value.
            - Must be six digits long
        - nightmeter (int, optional): The night meter value.
            - Must be six digits long
    """
    # Authentication fields
    username: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            pattern=r"^[A-Za-z0-9_]+$",
            min_length=5,
        ),
        Field(index=True, description="Authentication username.", unique=True),
    ]

    password: Annotated[str, Field(description="Hash of Authentication password")]

    # Additional fields
    email: Annotated[
        Optional[str],
        StringConstraints(
            pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        ),
        Field(
            default=None,
            description="Mail address for pwd recovery",
        ),
    ]
    sng_username: Annotated[
        Optional[str],
        StringConstraints(pattern=r"^[A-Za-z0-9_]+$"),
        Field(
            index=True,
            description="Electricity provider username."),
    ]
    sng_password: Annotated[
        Optional[str], Field(
            default=None,
            description="Electricity provider password")
    ]
    daymeter: Annotated[
        Optional[int],
        Field(
            default=None,
            description="Day meter endpoint number",
            ge=100000,
            le=999999
        ),
    ]
    nightmeter: Annotated[
        Optional[int],
        Field(
            default=None,
            description="Night meter endpoint number",
            ge=100000,
            le=999999
        ),
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
                }
            ]
        }
    }

    # # Validation
    # @field_validator("username", "sng_username")
    # @classmethod
    # def validate_usernames(cls, v: str, info: ValidationInfo) -> str:
    #     if len(v) < 5:
    #         raise ValueError(f"{info.field_name} must be at least 5 characters long")
    #     return v

    # @field_validator("password", "sng_password")
    # @classmethod
    # def validate_passwords(cls, v: str, info: ValidationInfo) -> str:
    #     if len(v) < 5:
    #         raise ValueError(f"{info.field_name} must be at least 5 characters long")
    #     return v

    # @field_validator("email")
    # @classmethod
    # def validate_email(cls, v: str, info: ValidationInfo) -> str:
    #     pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    #     if not re.match(pattern, v):
    #         raise ValueError(f"{info.field_name} must be a valid email address")
    #     return v

    # @field_validator("daymeter", "nightmeter")
    # @classmethod
    # def validate_meter(cls, v: str, info: ValidationInfo) -> str:
    #     if v and len(str(v)) != 6:
    #         raise ValueError(f"{info.field_name} number must be 6 characters long")
    #     return v
    

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


class DecodeToken(SQLModel):
    """Schema for token decoding.
    """
    username: Annotated[str,
                        Field(
                            description="Username from token")]
    #exp: Annotated[int, Field(description="Token expiration time")]

    model_config: ConfigDict = {
        'json_schema_extra': {
            'examples': [
                {
                    'username': 'dummy_user',
                }
            ]
        }
    }

class Response404(SQLModel):
    """Schema for query return error.
    """
    error: Annotated[
        str,
        Field(
            description='Error description'
            )
        ]
    info: Annotated[
        str,
        Field(
            description="Error details"),
    ]

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "User not found",
                    "info": "User `username` not found in db",
                }
            ]
        }
    }


class Response500(SQLModel):
    """Error schema for database exceptions."""

    error: Annotated[
        str,
        Field(
            description="Error description"
        ),
    ]
    info: Annotated[
        dict[str, str | Any],
        Field(
            description="Error details",
        ),
    ]

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "Database validation error",
                    "info": {
                        "username": {
                            "Input": "asd",
                            "Message": "String should have at least 5 characters",
                        },
                    },
                }
            ]
        }
    }


class UserResponseSchema(UserBase):
    """Response schema for user data.
    
    Add id field from database to response.
    """
    id: Annotated[int, "User id"]
    api_response: Annotated[
        Optional[Union[Response404, Response500]],
        Field(
            default=None,
            description="API response for error handling"
        ),
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
                    "api_response": "`null` for status code 200",
                }
            ]
        }
    }


class UserInputSchema(UserBase):
    """Input schema for user creation.
    """
    pass

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
                }
            ]
        }
    }
