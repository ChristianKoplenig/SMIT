"""Schemas for response formatting."""
from typing import Annotated, Any
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

class Response400(SQLModel):
    """Schema for bad data request."""

    error: Annotated[
        str, Field(description="Error description")
    ] = "Bad request error"
    info: Annotated[
        str,
        Field(description="Error details"),
    ]

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "Bad request error",
                    "info": "Username already exists in database.",
                }
            ]
        }
    }


class Response401(SQLModel):
    """Schema for authorization error."""
    error: Annotated[
        str,
        Field(description="Error description")] = 'Authorization error'
    info: Annotated[
        str,
        Field(description="Error details"),
    ]

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "Authorization error",
                    "info": "User `username` not registered",
                }
            ]
        }
    }

class Response404(SQLModel):
    """Schema for query return error."""

    error: Annotated[str, Field(description="Error description")]
    info: Annotated[
        str,
        Field(description="Error details"),
    ]

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "User not found",
                    "info": "User `username` not found in db",
                }
            ]
        }
    }

class Response422(SQLModel):
    """Error schema for invalid user input."""

    error: Annotated[
        str,
        Field(description="Error description"),
    ]
    info: Annotated[
        dict[str, str | Any],
        Field(
            description="Error details",
        ),
    ]

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "Input validation error",
                    "info": {
                        "username": {
                            "Input": "asd",
                            "Message": "String should have at least 5 characters",
                        },
                    },
                }
            ]
        }
    }

class Response500(SQLModel):
    """Error schema for database exceptions."""

    error: Annotated[
        str,
        Field(description="Error description"),
    ]
    info: Annotated[
        dict[str, str | Any],
        Field(
            description="Error details",
        ),
    ]

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "Database validation error",
                    "info": {
                        "username": {
                            "Input": "asd",
                            "Message": "String should have at least 5 characters",
                        },
                    },
                }
            ]
        }
    }
