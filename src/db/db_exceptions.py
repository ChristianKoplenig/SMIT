class DbExceptionLogger:
    """
    Manage database exceptions.
    """

    @staticmethod
    def logging_input(e: Exception) -> str:
        """Format general Exception.

        Args:
            e (Exception): The exception to be logged.

        Returns:
            str: The formatted error message.
        """
        error_type = type(e).__name__
        line_number = e.__traceback__.tb_lineno  # type: ignore
        method_name = e.__traceback__.tb_frame.f_code.co_name  # type: ignore
        e_arguments = e.args[0]
        error_message = f'Method: "{method_name}()" raised: "{error_type}" for input: "{e_arguments}" at line: {line_number}'
        return error_message


class DatabaseError(Exception):
    """Generate error message from traceback.

    Args:
        e (Exception): The exception to be logged.
        message (str): The custom error message to display.

    Returns:
        str: The formatted error message.
    """

    def __init__(self, e: Exception, message: str) -> None:
        self.message: str = message
        self.error: Exception = e

        self.error_details: str = self._create_error_message(e)

        self.proccessed_message: str = (
            f"{self.error_details}; Provided message: {self.message}"
        )

        super().__init__(self.message)

    def _create_error_message(self, e: Exception) -> str:
        """
        Creates the error message.

        Returns:
            str: The error message.
        """

        error_type: str = type(e).__name__
        method_name: str = e.__traceback__.tb_frame.f_code.co_name  # type: ignore
        error_argument: str = e.args[0]

        return f"Database Error in method: {method_name}(); Raised: {error_type} for input: {error_argument}"

    def __str__(self) -> str:
        return f"{self.proccessed_message}"


class DbEngineError(Exception):
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
        return f"Database Error: {self.message}"


class DbReadError(Exception):
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
        return f"Database Error: {self.message}"


class DbCreateError(Exception):
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
        return f"Database Error: {self.message}"


class DbUpdateError(Exception):
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
        return f"Database Error: {self.message}"


class DbDeleteError(Exception):
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
        return f"Database Error: {self.message}"
