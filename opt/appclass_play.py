import os
import pathlib as pl
import tomlkit

# Import Custom Modules
from SMIT.scrapedata import Webscraper
from SMIT.filepersistence import Persistence
from SMIT.rsahandling import RsaTools
from SMIT.filehandling import OsInterface, TomlTools
from SMIT.userinput import UiTools

class Application():
    """Main class for application setup.
    
    Load user configuration files.
    Initialize the folder structure.   
    Instantiate all custom modules.
    Set/store password according to user preference.
    """
    def __init__(self, dummy: bool=False) -> None:
        
        if dummy is False:
            # Load paths to user configuration files
            user_data = pl.Path('config/user_data.toml')
            user_settings = pl.Path('config/user_settings.toml')
        else:
            # Set path to dummy configuration
            user_data = pl.Path('config/dummy_data.toml')
            user_settings = pl.Path('config/dummy_settings.toml')
            print('Dummy configuration loaded')
        
        self._add_TOML_to_attributes(user_data)    
        self._add_TOML_to_attributes(user_settings)
        self._initialize_folder_structure()
        self._add_modules_to_attributes()
        
        if dummy is False:
            # No need for password entry in dummy configuration
            self._ask_for_password_if_not_stored()
    
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
        
    def _ask_for_password_if_not_stored(self) -> None:
        """Start password dialog if the password is not stored in `user_data.toml`.
        """
        # pylint: disable=no-member
        if not 'password' in self.Login:    
            self.gui.password_dialog()      
            
    def _initialize_folder_structure(self) -> None:
        """Create folder structure.
        
        If the needed folders do not exist they will be created.
        If the folders exist no error will be raised
        """
        # pylint: disable=no-member  
        for folder, folder_path in self.Folder.items():
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
    
    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"



##################### run ##############################    
app = Application()
#app.scrape.sng_login(app.Folder['raw_daysum'])