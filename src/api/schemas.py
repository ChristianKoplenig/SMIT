import re
from datetime import datetime
from typing import Annotated, Optional

from pydantic import StringConstraints, ValidationInfo, field_validator, BaseModel


class UserBaseSchema(BaseModel):
    """User model for api

    Attributes:
        id (Optional[int]): The unique identifier of the user.
        username (str): Authentication username; mandatory field for authenticator.
        password (str): Authentication password; mandatory field for authenticator.
        email (str, optional): The email address of the user.
        sng_username (str, optional): The username for energy provider login.
        sng_password (str, optional): The password for energy provider login.
        daymeter (str, optional): The day meter value.
        nightmeter (str, optional): The night meter value.
    """

    # Generated on commit
    id: Annotated[Optional[int], 'User id']
    created_on: Annotated[
        Optional[datetime],
        "User creation date"
    ]

    # Authentication fields
    username: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            pattern=r"^[A-Za-z0-9_]+$",
            min_length=5,
        ),
        'Username field for authentication'
    ]

    password: Annotated[str, 'Password field for authentication']

    # Additional fields
    # Define according to individual needs
    # Fields containing the string 'password' will be hashed automatically
    email: Annotated[
        Optional[str],
        StringConstraints(
            pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        ),
        'Mail address for pwd recovery'
    ]

    sng_username: Annotated[
        Optional[str],
        StringConstraints(pattern=r"^[A-Za-z0-9_]+$"),
        "Electricity provider username."
    ]
    sng_password: Annotated[
        Optional[str],
        "Elictricity provider password"
    ]
    daymeter: Annotated[
        Optional[int],
        StringConstraints(pattern=r"^\d{6}$"),
        "Day meter endpoint number", 
    ]
    nightmeter: Annotated[
        Optional[int],
        StringConstraints(pattern=r"^\d{6}$"),
        "Day meter endpoint number", 
    ]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

    # Validation
    @field_validator("username", "sng_username")
    @classmethod
    def validate_usernames(cls, v: str, info: ValidationInfo) -> str:
        if len(v) < 5:
            raise ValueError(f"{info.field_name} must be at least 5 characters long")
        return v

    @field_validator("password", "sng_password")
    @classmethod
    def validate_passwords(cls, v: str, info: ValidationInfo) -> str:
        if len(v) < 5:
            raise ValueError(f"{info.field_name} must be at least 5 characters long")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str, info: ValidationInfo) -> str:
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(pattern, v):
            raise ValueError(f"{info.field_name} must be a valid email address")
        return v

    @field_validator("daymeter", "nightmeter")
    @classmethod
    def validate_meter(cls, v: str, info: ValidationInfo) -> str:
        if len(str(v)) != 6:
            raise ValueError(f"{info.field_name} number must be 6 characters long")
        return v
