from typing import Any, TYPE_CHECKING
import traceback

if TYPE_CHECKING:
    from pydantic import ValidationError

class ApiValidationError(Exception):
    """Handle Pydantic ValidationError.

    Methods to handle Pydantic ValidationError exceptions.
    Format the error message and return a dictionary containing all errors.
    Use to generate human readable error message.

    Attributes:
        error: `ValidationError` exception class from Pydantic.
    """

    def __init__(self, e: "ValidationError") -> None:
        self.error = e
        super().__init__(self.error)

    def _format_validation_error(self) -> dict[str, str | Any]:
        """Format the validation error message.
        
        Output multiple validation error messages in one dictionary.

        Returns:
            dict[str, str]: 
                The formatted validation error message.
        """
        error_messages: dict[str, str | Any] = {}
        for error in self.error.errors():
            field: str = str(error["loc"][0])
            error_message: str = error["msg"]
            input: str = error["input"]
            error_messages[field] = {'Input': input, 'Message': error_message}
        return error_messages
    
    def message(self) -> dict[str, str | Any]:
        """Error message for API response.

        Example:
            ```json
            {
                "username": {
                    "Input": "du",
                    "Message": "Username length must be greater than 3"
                }
            }
            ```

        Usage:
            ```
            try:
                user: Schema = Schema.model_validate(usr)
            except ValidationError as ve:
                raise HTTPException(
                    status_code=400, detail=ApiValidationError(ve).message()
                )
            ```

        Returns:
            dict[str, str | Any]: The formatted validation error message.
        """
        return self._format_validation_error()
    
class DbSessionError(Exception):
    """Handle database session error.
    """

    def __init__(self, e: Exception) -> None:
        self.error: Exception = e
        super().__init__(self.error)

    def message(self) -> str:
        """Format the database session error message.

        Returns:
            str: The formatted database session error message.
        """
        error_type: str = type(self.error).__name__
        tb: traceback.TracebackException = traceback.TracebackException.from_exception(self.error)
        return f'Database session raised: "{error_type}" error for "{tb.stack[-1].name}".'
