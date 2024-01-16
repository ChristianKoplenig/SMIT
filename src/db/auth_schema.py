from typing import Optional
from datetime import datetime

from sqlmodel import Field, SQLModel
from typing_extensions import Annotated, Doc

from pydantic import StringConstraints

class AuthDbSchema(SQLModel, table=True):
    """
    Table for user management.

    Attributes:
        id (Optional[int]): The unique identifier of the user.
        username (str): Smit Application username.
        password (str): Smit Application password.
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
                        Doc("Smit application username."),
                        ] = Field(index=True,
                                  description="Smit application username.",
                                  unique=True,
                                  min_length=3)    
    
    password: str = Field(..., description=" Hash of Smit application password")
    
    # Additional fields
    email: Optional[str] = Field(default=None, description="Mail address for pwd recovery")
    sng_username: Optional[str] = Field(index=True, 
                                      description="Electricity provider username.") 
    sng_password: Optional[str] = Field(default=None, description="Elictricity provider password")
    daymeter: Optional[int] = Field(default=None, description="Day meter endpoint number")
    nightmeter: Optional[int] = Field(default=None, description="Night meter endpoint number")
    
    
