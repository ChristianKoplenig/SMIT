from pydantic import (BaseModel,
                      field_validator)
import re

from db.auth_schema import AuthDbSchema


class  User(BaseModel):

    auth_table: AuthDbSchema
        
    @field_validator('auth_table')
    @classmethod
    def validate_auth_table(cls, v: str) -> str:
        """
        Checks the validity of the entered username.

        Parameters
        ----------
        v: str
            The usernmame to be validated.
        Returns
        -------
        str
            Validity of entered username.
        """
        # Smit username
        smit_usr = v.username
        sng_usr = v.sng_username
        if len(smit_usr) < 3 or len(sng_usr) < 3:
            raise ValueError("Username must be at least 3 characters long")
        
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(pattern, v.email):
            raise ValueError("Invalid email address")   
        
        if len(str(v.daymeter)) != 6 or len(str(v.nightmeter)) != 6:
            raise ValueError("Meter number must be 6 characters long")
        
        return v
    
create_table = AuthDbSchema

smit_db = create_table(
    username= 'dummy_user',
    password= '$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om',
    email= 'dummy@dummymail.com',
    sng_username= 'dummy_sng_login',
    sng_password= 'dummy_sng_password',
    daymeter= 199996,
    nightmeter= 199997)




u = User(auth_table=smit_db)

print(u.model_dump())

print(u.auth_table.username)

# for key, value in u.model_dump().items():
#     print(key, value)
# #     #print(key, value)