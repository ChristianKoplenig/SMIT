from typing import Optional
from datetime import datetime

from sqlmodel import Field, SQLModel

class SmitAuth(SQLModel, table=True):
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

    id: Optional[int] = Field(default=None, primary_key=True)
        
    username: str = Field(description="Smit Application username")
    password: str = Field(description="Smit Application password")
    email: Optional[str] = Field(None, description="Mail address for pwd recovery")
    sng_username: Optional[str] = Field(None, description="Elictricity provider username")
    sng_password: Optional[str] = Field(None, description="Elictricity provider password")
    daymeter: Optional[str] = Field(None, description="Day meter endpoint number")
    nightmeter: Optional[str] = Field(None, description="Night meter endpoint number")
    
    created_on: Optional[datetime] = Field(default_factory=datetime.now, description="User creation date")
    
