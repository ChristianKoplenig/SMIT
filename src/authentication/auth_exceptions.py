import typing

if typing.TYPE_CHECKING:
    from pydantic import ValidationError
class AuthExceptionLogger:
    """
    A class that provides methods for logging exceptions.
    """

    @staticmethod
    def logging_input(e: Exception) -> str:
        """
        Logs the details of the given exception.

        Args:
            e (Exception): The exception to be logged.

        Returns:
            str: The formatted error message.
        """
        error_type = type(e).__name__
        line_number = e.__traceback__.tb_lineno # type: ignore
        method_name = e.__traceback__.tb_frame.f_code.co_name # type: ignore
        error_message = f'Method: "{method_name}()" raised: "{error_type}" for input: "{e.args[0]}" at line: {line_number}'
        return error_message
    
class AuthCreateError(Exception):
    """
    Exceptions raised for authentication API.

    Attributes
    ----------
    message: str
        The custom error message to display.
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"Authentication Error: {self.message}"

class AuthUpdateError(Exception):
    """
    Exceptions raised for authentication API.

    Attributes
    ----------
    message: str
        The custom error message to display.
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"Authentication Error: {self.message}"
    
class AuthWriteError(Exception):
    """
    Exceptions raised for authentication API.

    Attributes
    ----------
    message: str
        The custom error message to display.
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"Authentication Error: {self.message}"
    
class AuthReadError(Exception):
    """
    Exceptions raised for authentication API.

    Attributes
    ----------
    message: str
        The custom error message to display.
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"Authentication Error: {self.message}"

class AuthDeleteError(Exception):
    """
    Exceptions raised for authentication API.

    Attributes
    ----------
    message: str
        The custom error message to display.
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"Authentication Error: {self.message}"
    
class AuthCookieError(Exception):
    """
    Exceptions raised for authentication API.

    Attributes
    ----------
    message: str
        The custom error message to display.
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"Cookie Error: {self.message}"
    
class AuthFormError(Exception):
    """
    Exception used for frontend error message generation.

    Attributes
    ----------
    message: str
        The custom error message to display.
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"{self.message}"
    
class AuthValidateError(Exception):
    """Format Pydantic ValidationError.

    Attributes:
        error: ValidationError exception class from Pydantic.
        error_dict: 
            - Key: Field from pydantic schema.
            - Value: Pydantic error message.
    """
    def __init__(self, e: 'ValidationError') -> None:
        self.error = e
        self.error_dict = self._format_validation_error()
        
        super().__init__(self.error)
    
    def _format_validation_error(self) -> dict:
        error_messages = {}
        for error in self.error.errors():
            field = error['loc'][0]
            error_message = error['msg']
            error_messages[field] = error_message
        return error_messages