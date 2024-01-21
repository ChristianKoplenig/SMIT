from typing import Optional, List
from datetime import datetime
import re

from sqlmodel import Field, SQLModel, JSON, Column
from typing_extensions import Annotated, Doc

from pydantic import StringConstraints, ValidationInfo, field_validator

class AuthDbSchema(SQLModel, table=True):
    """
    Table for user management.

    Attributes:
        id (Optional[int]): The unique identifier of the user.
        username (str): Authentication username.
        password (str): Authentication password.
        email (str, optional): The email address of the user.
        sng_username (str, optional): The username for energy provider login.
        sng_password (str, optional): The password for energy provider login.
        daymeter (str, optional): The day meter value.
        nightmeter (str, optional): The night meter value.
    """
    __tablename__ = 'auth_dev'

    # Generated on commit
    id: Optional[int] = Field(default=None, primary_key=True)
    created_on: Optional[datetime] = Field(default_factory=datetime.now, description="User creation date")
    
    # Authentication fields
    username: Annotated[str, 
                        StringConstraints(strip_whitespace=True, 
                            to_lower=True, 
                            pattern=r'^[A-Za-z0-9_]+$'),
                        Doc("Authentication username."),
                        ] = Field(index=True,
                                  description="Authentication username.",
                                  unique=True)    
    
    password: str = Field(description="Hash of Authentication password")
    
    # Additional fields
    email: Optional[str] = Field(default=None, description="Mail address for pwd recovery")
    sng_username: Optional[str] = Field(index=True, 
                                      description="Electricity provider username.") 
    sng_password: Optional[str] = Field(default=None, description="Elictricity provider password")
    daymeter: Optional[int] = Field(default=None, description="Day meter endpoint number")
    nightmeter: Optional[int] = Field(default=None, description="Night meter endpoint number")
    
    # Validation
    @field_validator('username', 'sng_username')
    @classmethod
    def validate_usernames(cls, v: str, info: ValidationInfo) -> str:
        if len(v) < 5:
            raise ValueError(f"{info.field_name} must be at least 5 characters long")
        return v

    @field_validator('password', 'sng_password')
    @classmethod
    def validate_passwords(cls, v: str, info: ValidationInfo) -> str:
        if len(v) < 5:
            raise ValueError(f"{info.field_name} must be at least 5 characters long")
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str, info: ValidationInfo) -> str:
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(pattern, v):
            raise ValueError(f"{info.field_name} must be a valid email address")
        return v

    @field_validator('daymeter', 'nightmeter')
    @classmethod
    def validate_meter(cls, v: str, info: ValidationInfo) -> str:
        if len(str(v)) != 6:
            raise ValueError(f"{info.field_name} number must be 6 characters long")
        return v
    
class AuthConfigSchema(SQLModel, table=True):
    """
    Represents the authentication configuration schema.

    Attributes:
        id (Optional[int]): The ID of the configuration.
        created_on (Optional[datetime]): The creation date of the configuration.
        preauth_mails (Optional[list]): The list of preauthorized email addresses.

    Methods:
        validate_preauth(cls, v: str, info: ValidationInfo) -> str: 
            Validates the email addresses for .

    """

    __tablename__ = 'auth_config'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_on: Optional[datetime] = Field(default_factory=datetime.now, description="User creation date")
    
    preauth_mails: Optional[str] = Field(default=None,
                                     description="Preauthorized email addresses")
    
    # Needed for Column(JSON)
    class Config:
        arbitrary_types_allowed = True
    
    @field_validator('preauth_mails')
    @classmethod
    def validate_preauth(cls, v: str, info: ValidationInfo) -> str:
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(pattern, v):
            raise ValueError(f"{info.field_name} must be a valid email address")
        return v
    
    
