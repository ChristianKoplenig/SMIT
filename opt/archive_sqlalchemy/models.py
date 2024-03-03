# import re
# from datetime import datetime
# from typing import Annotated, Any, Optional

# from pydantic import StringConstraints, ValidationInfo, field_validator
# from sqlmodel import Field, SQLModel

# #TODO: / NOT NEEDED / Check if needed, switch to fastapi
# class AuthModel(SQLModel, table=True):
#     """
#     Table for user management.

#     Attributes:
#         id (Optional[int]): The unique identifier of the user.
#         username (str): Authentication username; mandatory field for authenticator.
#         password (str): Authentication password; mandatory field for authenticator.
#         email (str, optional): The email address of the user.
#         sng_username (str, optional): The username for energy provider login.
#         sng_password (str, optional): The password for energy provider login.
#         daymeter (int, optional): The day meter value.
#         nightmeter (int, optional): The night meter value.
#     """

#     __tablename__: Any = "auth_dev"

#     # Generated on commit
#     id: Annotated[Optional[int], Field(default=None, primary_key=True)]
#     created_on: Annotated[
#         Optional[datetime],
#         Field(default_factory=datetime.now, description="User creation date"),
#     ]

#     # Authentication fields
#     username: Annotated[
#         str,
#         StringConstraints(
#             strip_whitespace=True,
#             to_lower=True,
#             pattern=r"^[A-Za-z0-9_]+$",
#             min_length=5,
#         ),
#         Field(index=True, description="Authentication username.", unique=True),
#     ]

#     password: Annotated[str, Field(description="Hash of Authentication password")]

#     # Additional fields
#     # Define according to individual needs
#     # Fields containing the string 'password' will be hashed automatically
#     email: Annotated[
#         Optional[str],
#         StringConstraints(
#             pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
#         ),
#         Field(
#             default=None,
#             description="Mail address for pwd recovery",
#         ),
#     ]
#     sng_username: Annotated[
#         Optional[str],
#         StringConstraints(pattern=r"^[A-Za-z0-9_]+$"),
#         Field(index=True, description="Electricity provider username."),
#     ]
#     sng_password: Annotated[
#         Optional[str], Field(default=None, description="Elictricity provider password")
#     ]
#     daymeter: Annotated[
#         Optional[int],
#         Field(default=None, description="Day meter endpoint number", regex=r"^\d{6}$"),
#     ]
#     nightmeter: Annotated[
#         Optional[int],
#         Field(default=None, description="Day meter endpoint number", regex=r"^\d{6}$"),
#     ]

#     # Validation
#     @field_validator("username", "sng_username")
#     @classmethod
#     def validate_usernames(cls, v: str, info: ValidationInfo) -> str:
#         if len(v) < 5:
#             raise ValueError(f"{info.field_name} must be at least 5 characters long")
#         return v

#     @field_validator("password", "sng_password")
#     @classmethod
#     def validate_passwords(cls, v: str, info: ValidationInfo) -> str:
#         if len(v) < 5:
#             raise ValueError(f"{info.field_name} must be at least 5 characters long")
#         return v

#     @field_validator("email")
#     @classmethod
#     def validate_email(cls, v: str, info: ValidationInfo) -> str:
#         pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
#         if not re.match(pattern, v):
#             raise ValueError(f"{info.field_name} must be a valid email address")
#         return v

#     @field_validator("daymeter", "nightmeter")
#     @classmethod
#     def validate_meter(cls, v: str, info: ValidationInfo) -> str:
#         if len(str(v)) != 6:
#             raise ValueError(f"{info.field_name} number must be 6 characters long")
#         return v

# # STRUCTURE -> schemas/db_models.py
# # TODO: switch to fastapi
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
