"""Schemas for user management."""
from typing import Annotated, Any, Optional, Union

from schemas.response_schemas import Response404, DatabaseErrorResponse #, Response500
from pydantic import ConfigDict, StringConstraints
from sqlmodel import Field, SQLModel

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
        Field(index=True, description="Electricity provider username."),
    ]
    sng_password: Annotated[
        Optional[str], Field(default=None, description="Electricity provider password")
    ]
    daymeter: Annotated[
        Optional[int],
        Field(
            default=None, description="Day meter endpoint number", ge=100000, le=999999
        ),
    ]
    nightmeter: Annotated[
        Optional[int],
        Field(
            default=None,
            description="Night meter endpoint number",
            ge=100000,
            le=999999,
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

class UserResponseSchema(UserBase):
    """Response schema for user data.

    Add id field from database to response.
    """

    id: Annotated[int, "User id"]
    api_response: Annotated[
        Optional[Union[Response404, DatabaseErrorResponse]],
        Field(default=None, description="API response for error handling"),
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
    """Input schema for user creation."""

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




##################################################
class Username(SQLModel):
    """Base schema for username fields."""

    # username_in_db: Annotated[
    #     Optional[str | None],
    #     StringConstraints(
    #         strip_whitespace=True,
    #         to_lower=True,
    #         pattern=r"^[A-Za-z0-9_]+$",
    #         min_length=5,
    #     ),
    #     Field(index=True, description="Authentication username.", unique=True),
    # ]

    username_input: Annotated[
        Optional[str | None],
        str,
        StringConstraints(
            pattern=r"^[A-Za-z0-9_]+$",
            min_length=5,
        ),
        Field(description="Username unformatted", default=None),
    ]


class Password(SQLModel):
    """Base schema for password fields."""

    # password_in_db: Annotated[
    #     Optional[str | None],
    #     Field(description="Hash of Authentication password")
    # ]

    password_input: Annotated[
        Optional[str | None], Field(description="Password unformatted", default=None)
    ]


class Email(SQLModel):
    """Base schema for email fields."""

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


class LoginFormInput(Username, Password):
    """Base schema for login form input fields."""

    # class Config:
    #     schema_extra = {
    #         'exclude': {'username_in_db'}
    #     }

    # model_config: ConfigDict = {
    #     'json_schema_extra': {
    #         'exclude': ['username_in_db', 'password_in_db'],
    #     },
    # }
    # pass
    # username: Annotated[
    #     Username.username_input.type,
    #     'Username from input form'
    # ]
    # password: Annotated[
    #     Password,
    #     'Password from input form'
    # ]
    pass


class LoginFormOutput(UserBase):
    """Base schema for login form output fields."""

    logged_in: Annotated[bool | None, "User logged in status"]


# class UserInput(UserBase):
#     """Schema for creating a new user."""

#     pass