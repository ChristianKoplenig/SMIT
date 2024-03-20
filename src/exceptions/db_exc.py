"""Database exceptions formatting."""
from typing import Annotated, Any
from pydantic import ValidationError

from schemas.response_schemas import DatabaseErrorSchema

class DatabaseError(Exception):
    """
    Custom exception class for database errors.

    Args:
        e (Exception): Exception to format.
        message (str): Custom info on exception.

    Attributes:
        message (str): Custom info on exception.
        error (Exception): The original exception.
        error_type (str): The type of the original exception.

    Methods:
        __str__(): Returns a string representation of the exception.
        _integrity_error(): Formats the exception for IntegrityError.
        _general_exception(): Formats the exception for other types.
        http_message(): Returns a dictionary representation of the exception for HTTP response.

    """

    def __init__(
            self,
            e: Annotated[Exception | ValidationError, 'Exception to format'],
            message: Annotated[str, 'Custom info on exception'],
            ) -> None:
        
        self.message: str = message
        self.error: Exception | ValidationError = e
        self.error_type = type(e).__name__

    def __str__(self) -> str:
        if self.error_type == 'IntegrityError':
            return f'{self._integrity_error()}'
        if self.error_type == 'ValidationError':
            return f'{self._validation_error()}'
        else:
            return f"{self._general_exception()}"

    def _general_exception(self) -> DatabaseErrorSchema:
        """Format general exception.

        Returns:
            dict[str, Any]: A dictionary containing the formatted exception details.

        Examples:
            >>> db_exc = DatabaseError(e, "Custom message")
            >>> db_exc._general_exception()
            {
                "Type": "IntegrityError",
                "Message": "Custom message",
                "Info": "Key (id)=(1) already exists.",
                "Traceback": "method_name"
            }

        """
        method: tuple[str] = (self.error.__traceback__.tb_frame.f_code.co_name,)  # type: ignore

        msg = DatabaseErrorSchema(
            type=self.error_type,
            message=self.message,
            error=self.error.args[0],
            location=f"CRUD Method: `{method[0]}()` raised error.",
        )
        return msg

    def _integrity_error(self) -> DatabaseErrorSchema:
        """Format IntegrityError exception.

        Returns:
            dict[str, Any]: A dictionary containing the formatted exception details.

        Examples:
            >>> db_exc = DatabaseError(e, "Custom message")
            >>> db_exc._integrity_error()
            {
                "Type": "IntegrityError",
                "Message": "Custom message",
                "Info": "Key (id)=(1) already exists.",
                "Traceback": Method: "method_name" raised error.
            }

        """
        method: tuple[str] = self.error.__traceback__.tb_frame.f_code.co_name, # type: ignore

        msg = DatabaseErrorSchema(
            type=self.error_type,
            message=self.message,
            error=self.error.args[0].split("DETAIL:")[1],
            location= f'CRUD Method: `{method[0]}()` raised error.'
        )
        return msg
    
    def _validation_error(self) -> DatabaseErrorSchema:
        """Format Pydantic ValidationError exception.

        Returns:
            dict[str, Any]: 
                A dictionary containing the formatted exception details.

        Examples:
            >>> db_exc = DatabaseError(e, "Custom message")
            >>> db_exc._validation_error()
            {
                "type": "ValidationError",
                "message": "Custom message",
                "error": {
                    "username": {
                        "Input": "du",
                        "Message": "Username length must be greater than 3"
                    },
                    "email": {
                        "Input": "du.com",
                        "Message": "Field must be validate email address"
                    }
                },
                "location": "Method: `method_name()` raised error."
        """
        error_messages: dict[str, str | Any] = {}
        method: tuple[str] = (self.error.__traceback__.tb_frame.f_code.co_name,)  # type: ignore

        if type(self.error) == ValidationError:
            errors = self.error.errors()

            for error in errors:
                field: str = str(error["loc"][0])
                error_message: str = error["msg"]
                input: str = error["input"]
                error_messages[field] = {"Input": input, "Error": error_message}
            
            msg = DatabaseErrorSchema(
                type=self.error_type,
                message=self.message,
                error=str(error_messages),
                location=f"CRUD Method: `{method[0]}()` raised error.",
            )
            return msg
        else:
            msg = DatabaseErrorSchema(
                type=self.error_type,
                message=self.message,
                error='Unspecific validation error.',
                location=f"CRUD Method: `{method[0]}()` raised error.",
            )
            return msg

    def http_message(self)-> DatabaseErrorSchema:
        """Returns dict for HTTP response.

        Returns:
            dict[str, Any]: A dictionary containing the formatted exception details.

        Examples:
            >>> db_exc = DatabaseError(e, "Custom message")
            >>> db_exc.http_message()
            {
                "Type": "IntegrityError",
                "Message": "Custom message",
                "Info": "Key (id)=(1) already exists.",
                "Traceback": "method_name"
            }
        """
        if self.error_type == 'IntegrityError':
            return self._integrity_error()
        if self.error_type == 'ValidationError':
            return self._validation_error()
        else:
            return self._general_exception()
    


############# Example generic database exceptions ################
# class DbReadError(Exception):
#     """
#     Exceptions raised for the database connection.

#     Attributes
#     ----------
#     message: str
#         The custom error message to display.
#     """

#     def __init__(self, message: str) -> None:
#         self.message = message
#         super().__init__(self.message)

#     def __str__(self) -> str:
#         return f"Database Error: {self.message}"

##################################################################
        
        ######## dump ##########

# self.http_code: int = http_code

# self.error_details: str = self._create_error_message(e)

# self.proccessed_message: str = (
#     f"{self.error_details}; \n Application message: {self.message}"
# )

# super().__init__(self.message)


# def _create_error_message(self, e: Exception) -> str:
#     """Create the error message from traceback.

#     Returns:
#         str: Error message containing trace information.
#     """

#     error_type: str = type(e).__name__
#     method_name: str = e.__traceback__.tb_frame.f_code.co_name  # type: ignore
#     try:
#         error_argument: str = e.args[0]
#     except Exception:
#         error_argument = "No argument provided"

#     return f"Database Error in method: {method_name}(); \n Raised: {error_type} with error argument: {error_argument}"
