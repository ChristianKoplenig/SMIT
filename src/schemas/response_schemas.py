"""Schemas for response formatting."""
from typing import Annotated, Any, TYPE_CHECKING, Type
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict
from fastapi import HTTPException

if TYPE_CHECKING:
    from exceptions.db_exc import DatabaseError


class DatabaseErrorResponse(HTTPException):
    """Raise on DatabaseError.
    
    Format database error message for HTTP response.

    Attributes:
        dbe (DatabaseError): The original exception.
        status_code (int): The HTTP error code.

    Raises:
        HTTPException: On database error.
            Status code 404 - If error type 'NoResultFound'.
            Status code 500 - On general database error.
    """

    def __init__(
        self,
        dbe: Annotated['DatabaseError', "Class DatabaseError"],
        status_code: Annotated[int, "http error code"] = 500,
    ) -> None:
        self.dbe: 'DatabaseError' = dbe

        error: dict[str, Any] = self.unpack_error()

        if error["type"] == "NoResultFound":
            status_code = 404

        super().__init__(status_code=status_code, detail=error)

    def unpack_error(self) -> dict[str, Any]:
        """Unpack error details."""

        model: DatabaseErrorSchema = self.dbe.http_message()

        return model.model_dump()


class DatabaseErrorSchema(SQLModel):
    """Define details field for database error response."""

    type: Annotated[str, Field(description="Type of error")]
    message: Annotated[str, Field(description="Custom debug info")]
    error: Annotated[str, Field(description="Details from error call stack")]
    location: Annotated[str, Field(description="Name of method where error occurred")]

    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "detail": {
                        "type": "IntegrityError",
                        "message": "create user error",
                        "error": "  Key (username)=(dummy_user) already exists.",
                        "location": "Method: `create_user()` raised error.",
                    }
                }
            ]
        }
    }

#############################################################
#TODO    ########### rework ############
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


#############################################################
    ########### dump ############
# class Response500(SQLModel):
#     """Error schema for database exceptions."""

#     error: Annotated[
#         str,
#         Field(description="Error description"),
#     ]
#     info: Annotated[
#         dict[str, str | Any],
#         Field(
#             description="Error details",
#         ),
#     ]

#     model_config: ConfigDict = {
#         "json_schema_extra": {
#             "examples": [
#                 {
#                     "error": "Database validation error",
#                     "info": {
#                         "username": {
#                             "Input": "asd",
#                             "Message": "String should have at least 5 characters",
#                         },
#                     },
#                 }
#             ]
#         }
#     }