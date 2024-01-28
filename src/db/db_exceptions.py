class ExceptionLogger:
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
        line_number = e.__traceback__.tb_lineno
        method_name = e.__traceback__.tb_frame.f_code.co_name
        error_message = f'Method: "{method_name}()" raised: "{error_type}" for input: "{e.args[0]}" at line: {line_number}'
        return error_message
    
class ReadError(Exception):
    """
    Exceptions raised for the database connection.

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

class CreateError(Exception):
    """
    Exceptions raised for the database connection.

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
    
class UpdateError(Exception):
    """
    Exceptions raised for the database connection.

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
    
class DeleteError(Exception):
    """
    Exceptions raised for the database connection.

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