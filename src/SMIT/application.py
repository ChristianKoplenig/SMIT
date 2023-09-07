"""Provide core functionality.

- Generate dummy user
- Load user settings
- Create folder structure
- Initiate logging
- Instantiate modules
- Initiate credentials gui

Typical usage:

    app = Application()
    dummy_user = Application(True)
"""
import os
import logging
import pathlib as pl
import shutil
# 3rd party libraries
import tomlkit
# Import Custom Modules
from SMIT.scrapedata import Webscraper
from SMIT.filepersistence import Persistence
from SMIT.rsahandling import RsaTools
from SMIT.filehandling import OsInterface, TomlTools
from SMIT.userinput import UiTools

class Application:
    # pylint: disable=no-member
    """Create application framework.
    
    - Set paths variables to config files.
    - Read user setting from config files and assign to `self`.
    - On initial run create folder structure according to `./config/user_settings.toml`.
    - Initialize logging function according to `SMIT.application.Application._setup_logger`.
    - Instantiate modules and assign to `self`.
    
    Dummy User
    ----------
    - On each instantiation delete and newly create `./.dummy` folder.
    - Locally simulate application features without scraping.
    - No call of tkinter module - GUI

    Parameters
    ----------
    
    dummy : bool = False
        Flag for running with dummy user
    """
    def __init__(self, dummy: bool=False) -> None:
        
        # Attribute needed for scrape and move routine
        self.dummy = dummy
        
        if self.dummy is False:
            # Load paths to user configuration files
            self.user_data = pl.Path('config/user_data.toml')
            self.user_settings = pl.Path('config/user_settings.toml')
        else:
            # Load application with dummy configuration
            self._setup_dummy_user()
        
        self._add_TOML_to_attributes(self.user_data)    
        self._add_TOML_to_attributes(self.user_settings)
        self._initialize_folder_structure()
        self._setup_logger()
        self._add_modules_to_attributes()
        
        if dummy is False:
            # Load Gui Dialog
            self.gui.credentials_dialog()
        
        self.logger.info('Application with user "%s" instantiated', self.Login["username"])
    
    def _add_modules_to_attributes(self) -> None:
        """Read modules dict and assign it to self.
        
        Calls function _load_modules()
        In modules dict the custom modules are stored as key, value pairs.
        Loading the modules dict makes the custom methods easy accessible. 
        """ 
        for key, value in self._load_modules().items():
            setattr(self, key, value)
            
    def _add_TOML_to_attributes(self, file_path: pl.Path) -> None:
        """Read config file and assign parameters to self.
        
        Call `tomlkit` library and read parameters from a `.toml` file.
        Loop trough config file and assign parameters to self.

        Parameters
        ----------
        file_path : pure path object
            Path to `.toml` config file.
        """
        # load file
        with open(file_path, 'rb') as file:
            data = tomlkit.load(file)
        # assign parameters
        for key, value in data.items():
            setattr(self, key, value)

    def _initialize_folder_structure(self) -> None:
        """Create folder structure.
        
        If the needed folders do not exist they will be created.
        If the folders exist no error will be raised
        """
        # pylint: disable=no-member  
        for folder_path in self.Folder.values():
            os.makedirs(folder_path, exist_ok= True) 
        
    def _load_modules(self) -> dict:
        """Create a dict with all loaded modules.
        
        Assign trivial names to instantiated modules.
        """
        modules = dict([
            ('gui', UiTools(self)),
            ('rsa', RsaTools(self)),
            ('toml_tools', TomlTools(self)),
            ('os_tools', OsInterface(self)),
            ('persistence', Persistence(self)),
            ('scrape', Webscraper(self))          
        ])
        return modules
    
    def _setup_logger(self):
        """Configuration for logging
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s :: %(levelname)-8s :: [%(module)s:%(lineno)d] :: %(message)s')

        file_handler = logging.FileHandler(self.Path['log_file'])
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
    def _setup_dummy_user(self):
        """Create environment for testing purposes
        """
        # Reset dummy user on login
        dummy_data_folder = pl.Path('./.dummy').absolute()
        if dummy_data_folder.exists():
            shutil.rmtree(dummy_data_folder)
                    
        
        # Set paths for copying dummy files
        source_dummy_csv = pl.Path('./opt/dummy_user/').absolute()
        dest_dummy_csv = pl.Path('./.dummy/csv_raw/daily').absolute()
        dest_dummy_settings = pl.Path('./.dummy/config').absolute()
        
        # Create folder for dummy raw files
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

# for key, value in __pdoc__.items():
#     if key.__contains__('__') and isinstance(value, type):
#         __pdoc__[key] = False
        #print(f'key: {key} value: {value}\n')

#print(__pdoc__.items())
