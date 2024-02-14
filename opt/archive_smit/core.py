"""Provide core functionality.

---

- Generate dummy user
- Load user settings
- Create folder structure
- Initiate logging
- Instantiate modules
- Open credentials gui

Typical usage:

    app = Application()
    dummy_app = Application(True)
"""
import os
import logging
import pathlib as pl
import shutil
# 3rd party libraries
import tomlkit
# Import Custom Modules
from smit.scrapedata import Webscraper
from smit.filepersistence import Persistence
from smit.rsahandling import RsaTools
from smit.filehandling import OsInterface, TomlTools


class Application:
    # pylint: disable=no-member
    """Create application framework.

    Full usage
    ----------
    - Set paths to user configuration files.
    - Assign user settings from config files to the application instance.
    - On initial run create folder structure according to `./config/user_settings.toml`.
    - Configure logging function.
    - Instantiate modules and assign to application instance.

    Dummy usage
    -----------
    Use for demonstration and testing.  
    
    - Run application with local data. 
    - No scraping functionality.
    - No call of tkinter module -> No GUI is loaded.
    - On each instantiation delete and newly create `./.dummy` folder.
    - Static data source: `./opt/dummy_user`.
    - Root directory: `./dummy`. 

    Attributes:
        dummy (bool = False): Flag for activating dummy run.
    """
    def __init__(self, dummy: bool = False) -> None:

        # Attribute needed for scrape and move routine
        self.dummy = dummy

        # Logging, Path hardcoded because of init order
        logfilepath = './log/app.log'
        self._setup_logger(logfilepath)
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.info(msg)

        if self.dummy is False:
            # Load paths to user configuration files
            self._copy_userdata_template()
            self.user_data = pl.Path('config/user_data.toml')
            self.user_settings = pl.Path('config/user_settings.toml')
        else:
            # Load application with dummy configuration
            self._setup_dummy_user()

        self._add_TOML_to_attributes(self.user_data)
        self._add_TOML_to_attributes(self.user_settings)
        self._initialize_folder_structure()
        self._add_modules_to_attributes()

        self.logger.info(f'Application with user {self.Login["username"]} instantiated.')

    def _add_modules_to_attributes(self) -> None:
        """Assign modules to application instance.

        Calls function `SMIT.application.Application._load_modules()`  
        Iterates over key, value pairs in modules dict 
        and assigns the module instances to the application instance.
        Make modules callable via keys in modules dict.
        """
        for key, value in self._load_modules().items():
            setattr(self, key, value)

        self.logger.info('All modules added to user instance')

    def _add_TOML_to_attributes(self, file_path: pl.Path) -> None:
        """Read config file and assign parameters to application instance.

        Call `tomlkit` library and read parameters from a `.toml` file.  
        Loop trough the file and assign all parameters to the application instance.

        Parameters
        ----------
        file_path : pathlib.Path
            Path to `.toml` config file.
        """
        # load file
        with open(file_path, 'rb') as file:
            data = tomlkit.load(file)
        # assign parameters
        for key, value in data.items():
            setattr(self, key, value)

        self.logger.debug(f'Attributes from {file_path} added to application instance.')

    def _initialize_folder_structure(self) -> None:
        """Create folder structure.

        Iterate over the folder table in settings file.  
        If a folder does not exist it will be created.    
        If the folders exists no error will be raised.  
        """
        # pylint: disable=no-member
        for folder_path in self.Folder.values():
            os.makedirs(folder_path, exist_ok=True)

        self.logger.debug('Folderstructure checked and initialized.')
            
    def _copy_userdata_template(self) -> None:
        """Initialize user data config
        
        On first run copy a user_data template to
        config folder.
        """
        src = './opt/app_setup/user_data.toml'
        dest = './config/user_data.toml'
        if not pl.Path(dest).exists():
            shutil.copy2(src, dest)

            self.logger.debug(f'User data template copied from: {src} to: {dest}')
            

    def _load_modules(self) -> dict:
        """Create dict with all modules.
        
        This method exists to assure that each module
        is instatiated just once. Additionally the 
        dicitionary is used in the test setup to check if
        all modules are loaded.        
        
        Instantiate all custom modules.  
        Assign trivial names to instantiated modules via keys.  
        
        Returns
        -------
        dict
            Dictionary where keys are trivial names and values
            are intantiated modules objects.
        """
        modules = dict([
            ('rsa', RsaTools(self)),
            ('toml_tools', TomlTools(self)),
            ('os_tools', OsInterface(self)),
            ('persistence', Persistence(self)),
            ('scrape', Webscraper(self))
        ])

        self.logger.debug('All Modules instantiated')

        return modules

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
        
    def _setup_dummy_user(self):
        """Create environment for testing purposes.
        
        This option will not run any scraping routines
        or GUI dialogs. It is intended to use for demonstration
        and for unit testing.
        
        - On each call delete `.dummy` folder.
        - Recreate folder and populate it with clean data.
        - Source for dummy data is `./opt/dummy_user`.
        - Set config path to `./.dummy/config`
        """
        # Reset .dummy folder
        dummy_data_folder = pl.Path('./.dummy').absolute()
        if dummy_data_folder.exists():
            shutil.rmtree(dummy_data_folder)

        # Set paths for copying dummy files
        source_dummy_csv = pl.Path('./opt/dummy_user/').absolute()
        dest_dummy_csv = pl.Path('./.dummy/csv_raw/daily').absolute()
        dest_dummy_settings = pl.Path('./.dummy/config').absolute()

        # Create folders which are needed before user init 
        # Rest will be created with Application.__init__
        dest_dummy_csv.mkdir(parents=True, exist_ok=True)
        dest_dummy_settings.mkdir(parents=True, exist_ok=True)

        # Copy csv files
        for filename in source_dummy_csv.glob('*.csv'):
            dest = dest_dummy_csv / filename.name
            shutil.copy2(filename, dest)
        # Copy settings files
        for filename in source_dummy_csv.glob('*.toml'):
            dest = dest_dummy_settings / filename.name
            shutil.copy2(filename, dest)

        # Set paths to dummy configuration
        self.user_data = pl.Path('./.dummy/config/dummy_data.toml')
        self.user_settings = pl.Path('./.dummy/config/dummy_settings.toml')

        # Logging
        self.logger.info('Dummy user initiated')

    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"


# Pdoc config get underscore methods
__pdoc__ = {name: True
            for name, classes in globals().items()
            if name.startswith('_') and isinstance(classes, type)}

__pdoc__.update({f'{name}.{member}': True
                 for name, classes in globals().items()
                 if isinstance(classes, type)
                 for member in classes.__dict__.keys()
                 if member not in {'__module__', '__dict__',
                                   '__weakref__', '__doc__'}})

__pdoc__.update({f'{name}.{member}': False
                 for name, classes in globals().items()
                 if isinstance(classes, type)
                 for member in classes.__dict__.keys()
                 if member.__contains__('__') and member not in {'__module__', '__dict__',
                                                                 '__weakref__', '__doc__'}})
