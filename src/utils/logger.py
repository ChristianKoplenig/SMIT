import inspect
import logging
import os

class ClassnameFilter(logging.Filter):
    """Injects contextual information into the logging.Formatter.
    """
    def filter(self, record):
        frame = inspect.currentframe().f_back  # type: ignore
        while frame:
            filename = inspect.getfile(frame)
            frame_self = frame.f_locals.get("self", None)
            if frame_self is not None:
                class_name = frame_self.__class__.__name__
                if class_name not in [
                    "Logger",
                    "ClassnameFilter",
                ] and not filename.endswith("logger.py"):
                    record.classname = class_name
                    record.lineno = frame.f_lineno
                    break
            frame = frame.f_back
        return True

class Logger(ClassnameFilter):
    """Application logger.

    Setup a logger with a file handler and a console handler.
    Use custom filter for class name and line number in format handler.
    Provide standard message for module initialization.

    Attributes:
    -----------
    logger (logging.Logger): The logger object used for logging.

    Methods:
    --------
    __init__(): Initializes the Logger object.
    _setup_logger(filepath): Configures the logger with file handler and console handler.
    log_module_init(): Logs a debug message on successful module initialization.

    """

    def __init__(self) -> None:
        # Logging, Path hardcoded because of init order
        logfilepath = "./log/app.log"
        self._setup_logger(logfilepath)

    def _setup_logger(self, filepath) -> None:
        """Configuration for logging.

        The default log folder is `./log` and the logfile is called `app.log`.
        Set logging levels for the log file is done via `file_handler.setLevel()`.
        Set logging levels for terminal output is done via `console_handler.setLevel()`.

        Logging Levels:
        ---------------
        - DEBUG
        - INFO
        - WARNING
        - ERROR
        - CRITICAL

        Args:
        ------
        filepath (str): The path to the log file.

        """
        # Create log file on init
        os.makedirs("./log", exist_ok=True)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Log message format
        self.logger.addFilter(ClassnameFilter())
        formatter = logging.Formatter(
            "%(asctime)s :: %(levelname)-8s :: [%(classname)s:%(lineno)d] :: %(message)s"
        )

        file_handler = logging.FileHandler(filepath)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        # Attach logger handlers just once
        if not self.logger.hasHandlers():
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def log_module_init(self) -> None:
        """Debug log entry on successful module initialization.

        Retrieves the class name and module name of the calling object.

        Example usage:
            logger.log_module_init()

        """
        if inspect.currentframe() is not None:
            frame = inspect.currentframe().f_back # type: ignore
            classname = frame.f_locals.get('self').__class__.__name__ # type: ignore
            module = frame.f_locals.get("self").__class__.__module__ # type: ignore

        # Message on successful module initialization
        msg = f"Class {classname} of the "
        msg += f"module {module} "
        msg += "successfully initialized."
        self.logger.debug(msg)