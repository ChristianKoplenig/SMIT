"""Database exceptions formatting."""
from typing import Annotated, Any
from utils.logger import Logger

class DatabaseError(Exception):
    """Generate database error message.

    Args:
        e (Exception): The exception to be logged.
        message (str): The custom error message to append.

    Returns:
        str: The formatted error message.
    """

    def __init__(
            self,
            e: Annotated[Exception, 'Exception to format'],
            message: Annotated[str, 'Custom info on exception'],
            ) -> None:
        
        self.message: str = message
        self.error: Exception = e
        self.error_type = type(e).__name__
        #self.http_code: int = http_code

        # self.error_details: str = self._create_error_message(e)

        # self.proccessed_message: str = (
        #     f"{self.error_details}; \n Application message: {self.message}"
        # )

        #super().__init__(self.message)



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



    def __str__(self) -> str:
        if self.error_type == 'IntegrityError':
            return f'{self._integrity_error()}'
        else:
            return f"{self._general_exception()}"
    

       
    def _integrity_error(self) -> dict[str, Any]:

        msg: dict[str, Any] = {
            "Type": self.error_type,
            "Message": self.message,
            "Info": self.error.args[0].split("DETAIL:")[1],
            "Traceback": self.error.__traceback__.tb_frame.f_code.co_name, # type: ignore
        }
        return msg

    def _general_exception(self) -> dict[str, Any]:
        msg: dict[str, Any] = {
            "Type": self.error_type,
            "Message": self.message,
            "Info": self.error.args[0],
            "Traceback": self.error.__traceback__.tb_frame.f_code.co_name, # type: ignore
        }
        return msg



    def http_message(self):
        if self.error_type == 'IntegrityError':
            return self._integrity_error()
        else:
            return self._general_exception()
    





# class DbEngineError(Exception):
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


# class DbCreateError(Exception):
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


# class DbUpdateError(Exception):
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


# class DbDeleteError(Exception):
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
