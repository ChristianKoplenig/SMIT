import os
import pathlib as pl
import tomlkit

# Import Modules
from SMIT.scrapedata import Webscraper
from SMIT.filepersistence import Persistence
from SMIT.rsahandling import RsaTools
from SMIT.filehandling import OsInterface, TomlTools
from SMIT.userinput import UiTools

class Application:
    """Init user
    """
    def __init__(self) -> None:
        print('Application init')
        print('################')
        
        # path to input file
        user_data = pl.Path('config/user_data.toml')
        user_settings = pl.Path('config/user_settings.toml')
        
        self.__add_TOML_to_attributes(user_data)    
        self.__add_TOML_to_attributes(user_settings)
        self.__initialize_folder_structure()
        self.__add_Modules_to_attributes()
        self.__ask_for_password_if_not_stored()
    
    def __add_Modules_to_attributes(self) -> None:        
        # loop throught modlues and assign to self
        for key, value in self.load_modules().items():
            setattr(self, key, value)
        print('Modules added to self')
        print('#####################')
            
    def __add_TOML_to_attributes(self, file_path):
        # load file
        with open(file_path, 'rb') as file:
            data = tomlkit.load(file)
        # loop through all key value pairs of the config file
        # and set them as attributes of the class
        for key, value in data.items():
            setattr(self, key, value)
        print('TOML added to self')
        print('##################')
        
    def __ask_for_password_if_not_stored(self):
        """Start password dialog if the password is not stored in `user_data`
        """
        # pylint: disable=no-member
        if not 'password' in self.Login:    
            self.gui.password_dialog()      


    ################## Folders ########################
    def __initialize_folder_structure(self):
        """Create all needed folders
        """
        # pylint: disable=no-member
        # folders = [
        #     self.Folder['raw_daysum'],
        #     self.Folder['raw_15min'],
        #     self.Folder['log'],
        #     self.Folder['work_daysum'],
        #     self.Folder['work_15min'],        
        #     self.Folder['config']            
        # ]
        
        print('folder_init loaded')
        # print(f"folder list: {folders}")
        print('##################')
        
        for folder, folder_path in self.Folder.items():
            os.makedirs(folder_path, exist_ok= True)
            print(f"folder checked: {folder}")
        
        print('\n')
        
                        
    # user as dict, maybe just for developing   
    def user_dict(self) -> dict:
        """assignes all self attributes to dict
        """
        user = {}
        for key, value in vars(self).items():
            user[key] = value
        return user
    
    def load_modules(self):
        """load custom modules and instantiate
        """
        
        modules = dict([
            ('gui', UiTools(self)),
            ('rsa', RsaTools(self)),
            ('toml_tools', TomlTools(self)),
            ('os_tools', OsInterface(self)),
            ('persistence', Persistence(self)),
            ('scrape', Webscraper(self))          
        ])
        print('Modules loaded')
        for key, value in modules.items():
            print(f"{key} - {value}")
        print('##############')
        return modules
    
    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"