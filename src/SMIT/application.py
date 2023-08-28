"""
Initialize Core Functionality
"""
import os
import pathlib as pl
import tomlkit

class Application:
    """Root level setup.
    
    Create folders
    Instatiate user
    
    """
    def __init__(self,
                 user_settings = pl.Path('./user_settings.toml'),
                 user_data = pl.Path('./user_data.toml')):
        
        # # Load data from configuration files
        # with open(user_settings, mode='rt') as file:
        #     self.settings = tomlkit.parse(file.read())
        # with open(user_data, mode='rt') as file:
        #     self.data = tomlkit.parse(file.read())
        # print('Configuration files loaded')
        # print('##########################')
        
        
        self.__instantiate_user()
        
        print(type(self))
        print(vars(self))
        
    # Concat data from files
    def __instantiate_user(self):
        """Create user instance
        """
        user_file = pl.Path('config/user_file.toml')
        
        with open(user_file, 'rb') as file:
            user_data = tomlkit.load(file)
            
        for key, value in user_data.items():
            setattr(self, key, value)
            
        print('User instantiated')
        print('#################')
        return self
        
        
        # self.user.body.extend(self.data.body)
        # self.user.body.extend(self.settings.body)
        
        # with open(self.user_file, mode='w') as file:
        #     tomlkit.dump(self.user, file)
        # print('########')
        # print('User created')
        
        
        
        
        
        #return tomlkit.load(self.user_file)    
    # def load_user(self):
    #     with open(self.user_file, mode='rt') as file:
    #         user = tomlkit.load(file)
    #         return user
    

    def url(self):
        url = self.Login['url']
        return url

    ################## Folders ########################
    def folder_init(self):
        """Create all needed folders
        """
        folders = [
            self.settings['Folder']['raw_daysum'],
            self.settings['Folder']['raw_15min'],
            self.settings['Folder']['log'],
            self.settings['Folder']['work_daysum'],
            self.settings['Folder']['work_15min'],
            self.settings['Folder']['keys'],            
            self.settings['Folder']['config']            
        ]
        
        print('#######')
        print('folder_init loaded')
        print(f"folder list: {folders}")
        
        for folder in folders:
            os.makedirs(folder, exist_ok= True)
            print(f"folder checked: {folder}")
        
        print('\n')
    
    ################### Modules ##########################    
    def imports(self):
        """Initialize Modules, Instaniate Classes
        """
        print('imports called')
        from modules.scrapedata import Webscraper
    
    
    ################## Debug ###########################    
    # def debbug_print(self):    
    #     #print(self.settings)
    #     print(vars(self.user))
    #     print(self.user['Key Login']['url'])
    #     print('\n')
 
 
 
###################### Run ###############################        
# user = Application().load_user()
# print(vars(user))
#Application()
print('Outside')
print('#######')
# print(Application().Login['username'])

class inherit_test(Application):
    def __init__(self):
        super().__init__()
        print('From inherit')
        print('############')
        print(self.Login['username'])

class inherit2_test(Application):
    def __init__(self):
        user = super().url()
        print('From inherit2')
        print('############')
        print(type(user))
    #print(user)    
inherit_test()
inherit2_test()
        