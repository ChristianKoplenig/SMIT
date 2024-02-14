"""Provide logging functionality.
"""
import os
import logging

class SmitLogger:
    """SMIT logging functionality.
    """
    def __init__(self) -> None:

        # Logging, Path hardcoded because of init order
        logfilepath = './log/app.log'
        self._setup_logger(logfilepath)

        # Create init log entry
        self.log_module_init(self)


        
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
        """
        # Create log file on init
        os.makedirs('./log', exist_ok=True)
        
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s :: %(levelname)-8s :: [%(module)s:%(lineno)d] :: %(message)s')

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
            
    def log_module_init(self, init_self) -> None:
        """Generate log entry for module init.

        This method generates a log message indicating that the class
        of the module has been successfully initialized.

        Returns:
            None
        """
        msg = f'Class {init_self.__class__.__name__} of the '
        msg += f'module {init_self.__module__} '
        msg += 'successfully initialized.'
        self.logger.debug(msg)

    def debug(self, msg: str, init_self) -> None:
        """Generate log entry with DEBUG level.

        Args:
            msg (str): The message to be logged.

        Returns:
            None
        """
        
        self.logger.debug(f'Class: {self.__class__.__name__}, Message: {msg}')
        
    # #### Check if this is needed?
    # # Return Logger
    # def get_logger(self) -> logging.Logger:
    #     """Return logger.
        
    #     Returns
    #     -------
    #     logging.Logger
    #         The logger.
    #     """
    #     return self.logger

    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"

#SmitLogger()