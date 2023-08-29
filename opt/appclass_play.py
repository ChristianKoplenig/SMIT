import sys
import os
import pathlib as pl
import tomlkit
from pprint import pprint

# #####################################################
# # Add custom modules path to sys.path and import
# module_dir = pl.Path("__file__").resolve().parent

# if sys.path[0] != str(module_dir):
#     sys.path.insert(0, str(module_dir))
# #####################################################

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
        #self.__initialize_folder_structure()
        self.__add_Modules_to_attributes()
        #self.__ask_for_password_if_not_stored()
    
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
        folders = [
            self.Folder['raw_daysum'],
            self.Folder['raw_15min'],
            self.Folder['log'],
            self.Folder['work_daysum'],
            self.Folder['work_15min'],        
            self.Folder['config']            
        ]
        
        print('folder_init loaded')
        # print(f"folder list: {folders}")
        print('##################')
        
        for folder in folders:
            os.makedirs(folder, exist_ok= True)
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
        from SMIT.scrapedata import Webscraper
        from SMIT.filepersistence import Persistence
        from SMIT.rsahandling import RsaTools
        from SMIT.filehandling import OsInterface, TomlTools
        from SMIT.userinput import UiTools
        
        modules = dict([
            ('gui', UiTools(self)),
            ('rsa', RsaTools(self)),
            ('toml_tools', TomlTools(self)),
            ('os_tools', OsInterface(self)),
            ('persistence', Persistence(self)),
            ('scrape', Webscraper(self))          
        ])
        print('Modules loaded')
        print('##############')
        return modules




################### testing ######################        
app = Application()
user = app.user_dict()
#scrape = app.load_modules()['scrape']
#modules = app.load_modules()
# for item in app.load_modules():
#     #print(type(item))
#     print(item.__class__.__name__)
#     modules[item] = item 
#     #print(value)
pprint(user, indent=4)
print('###################')
#print('gui: ' + str(type(modules['gui'])))
#print('rsa: ' + str(type(modules['rsa'])))
print('####################')
#print(dict(modules))
#print('rsa: ' + str(modules['rsa']))
#gui, rsa, toml_tools, os_tools, persistence, scrape = modules

# gui = modules['rsa']
# print(gui.__class__)
# print(str(gui.encrypt_pwd('test')))


# print(type(os_tools))
# print(modules)

# scrape.stromnetz_setup(user['Folder']['raw_daysum'], False)

#print(str(modules))
#print(type(scrape))

#print(user['Folder']['raw_daysum'], False)
#modules['scrape'].stromnetz_setup(user['Folder']['raw_daysum'], False)