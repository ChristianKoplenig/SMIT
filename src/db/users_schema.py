from typing import Optional

from sqlmodel import Field, SQLModel

class SmitUser(SQLModel, table=True):
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
    __tablename__ = 'auth'

    id: Optional[int] = Field(default=None, primary_key=True)
        
    username: str
    password: str
    email: Optional[str] = None
    sng_username: Optional[str] = None
    sng_password: Optional[str] = None
    daymeter: Optional[str] = None
    nightmeter: Optional[str] = None
    
    #created_on: Optional[datetime] = datetime.now
    
