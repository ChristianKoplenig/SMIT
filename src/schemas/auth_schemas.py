"""Extra schemas for authentication component."""
from typing import Annotated
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

class AuthToken(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    """Schema for token decoding."""

    username: Annotated[str, Field(description="Username from token")]

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "dummy_user",
                }
            ]
        }
    }