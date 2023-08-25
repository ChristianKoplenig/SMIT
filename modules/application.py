"""
Initialize Core Functionality
"""
import os
import pathlib as pl
import tomlkit

class BaseClass:
    """Root level setup.
    
    Create folders
    
    """
    def __init__(self) -> any:
        
        self.user_settings = pl.Path('./user_settings.toml')
        self.folders = []
        # Load data from file
        with open(self.user_settings, mode='rt', encoding='utf-8') as file:
            self.settings = tomlkit.load(file)
        print('#######')
        print('Toml file loaded')
        print(self.settings['Folder']['raw_daysum'])
        print('\n')

    def folder_init(self):
        """Create all needed folders
        """
        self.folders = [
            self.settings['Folder']['raw_daysum'],
            self.settings['Folder']['raw_15min'],
            self.settings['Folder']['log'],
            self.settings['Folder']['work_daysum'],
            self.settings['Folder']['work_15min'],
            self.settings['Folder']['keys']            
        ]
        
        for folder in self.folders:
            os.makedirs(folder, exist_ok= True)
            print(f"folder created: {folder}")
        print('#######')
        print('folder_init loaded')
        print(self.folders)
        print('\n')
        
        
BaseClass().folder_init()           
        # folders
        # folders = [
            
        # ]
        
        
###############################
    # def load_toml_file(self, filename: pl.Path) -> tomlkit:
    #     """Read `.toml` file and return Python TOML object.

    #     Parameters
    #     ----------
    #     filename : pl.Path
    #         Path object to the `.toml` file.

    #     Returns
    #     -------
    #     object
    #         Python TOML object
    #     """
    #     with open(filename, mode='rt', encoding='utf-8') as file:
    #         data = tomlkit.load(file)        
        
    #     return data 