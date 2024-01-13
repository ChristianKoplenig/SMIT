import re
from pydantic import BaseModel, field_validator

# Schema for data validation
from db.auth_schema import SmitAuth as AuthTableSchema

class AuthCredentials(BaseModel):
    """
    Schema for user management.

    Attributes:
        users (pydantic.Model): Database schema for authentication data.
        cookie_name: str
            The name of the JWT cookie stored on the client's browser for passwordless reauthentication.
        key: str
            The key to be used for hashing the signature of the JWT cookie.
        cookie_expiry_days: float
            The number of days before the cookie expires on the client's browser.
        preauthorized: list
            The list of emails of unregistered users authorized to register.
        validator: Validator
            A Validator object that checks the validity of the username, name, and email fields.
    """
    db_schema: AuthTableSchema
    cookie_name: str = 'streamlit-smit-app'
    key: str = 'cookey'
    cookie_expiry_days: float = 30
    preauthorized: list = []

    @field_validator('db_schema')
    @classmethod
    def validate_auth_table(cls, v: str) -> str:
        """
        Validates the authentication table.
        Args:
            v (str): The authentication table to be validated.
        Raises:
            ValueError: If the username is less than 3 characters long.
            ValueError: If the email address is invalid.
            ValueError: If the meter number is not 6 characters long.
        Returns:
            str: The validated authentication table.
        """
        # Smit username
        smit_usr = v.username
        sng_usr = v.sng_username
        if len(smit_usr) < 3 or len(sng_usr) < 3:
            raise ValueError("Username must be at least 3 characters long")
        
        # Standard email address validation
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(pattern, v.email):
            raise ValueError("Invalid email address")   
        
        # Additional validation for use case specific fields
        # Length of meter number
        if len(str(v.daymeter)) != 6 or len(str(v.nightmeter)) != 6:
            raise ValueError("Meter number must be 6 characters long")
        return v
        
    @field_validator('preauthorized')
    @classmethod
    def validate_preauthorized(cls, v: str) -> str:
        """
        Validates the preauthorized list.

        Args:
            v (str): The preauthorized list to be validated.

        Raises:
            ValueError: If the email address is invalid.

        Returns:
            str: The validated preauthorized list.
        """
        for email in v:
            pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if not re.match(pattern, email):
                raise ValueError("Invalid email address in preauthorized list") 
        return v

######### Debug
# create_user = AuthTableSchema

# # Smit instance
# smit_db = create_user(
#     username= 'dummy_user',
#     password= '$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om',
#     email= 'dummy@dummymail.com',
#     sng_username= 'dummy_sng_login',
#     sng_password= 'dummy_sng_password',
#     daymeter= 199996,
#     nightmeter= 199997)

# a = AuthCredentials(db_schema=smit_db)

# print(a.model_dump())

# for name, value in a.db_schema:
#     print(f"{name}: {value}")