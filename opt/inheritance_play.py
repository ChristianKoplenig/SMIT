import sys
import pathlib as pl
import tomlkit
# Add custom modules path to sys.path and import
module_dir = pl.Path("__file__").resolve().parent

if sys.path[0] != str(module_dir):
    sys.path.insert(0, str(module_dir))

class Application:
    """Init user
    """
    def __init__(self) -> None:
        print('Application init')
        print('################')
        
        # path to input file
        user_file = pl.Path('config/user_file.toml')
        
        # set self attributes
        with open(user_file, 'rb') as file:
            user_data = tomlkit.load(file)
        
        # loop through all key value pairs of the config file
        # and set them as attributes of the class            
        for key, value in user_data.items():
            setattr(self, key, value)
    
    # user as dict    
    def user_dict(self) -> dict:
        """assignes all self attributes to dict
        """
        user = {}
        for key, value in vars(self).items():
            user[key] = value
        return user
    
    def load_modules(self):
        """load custom modules and instaniate
        """
        from modules.scrapedata import Webscraper
        from modules.filepersistence import Persistence
        from modules.rsahandling import RsaTools
        from modules.filehandling import OsInterface, TomlTools
        from modules.userinput import UiTools
        
        gui = UiTools(self)
        rsa = RsaTools(self)
        toml_tools = TomlTools(self)
        os_tools = OsInterface(self)
        persistence = Persistence(self)
        scrape = Webscraper(self)
        return gui, rsa, toml_tools, os_tools, persistence, scrape
        
app = Application()
user = app.user_dict()
#scrape = app.load_modules()['scrape']
modules = app.load_modules()
# for item in app.load_modules():
#     #print(type(item))
#     print(item.__class__.__name__)
#     modules[item] = item 
#     #print(value)

gui, rsa, toml_tools, os_tools, persistence, scrape = modules

print(type(os_tools))
print(modules)

scrape.stromnetz_setup(user['Folder']['raw_daysum'], False)

#print(str(modules))
#print(type(scrape))

#print(user['Folder']['raw_daysum'], False)
#scrape.stromnetz_setup(user['Folder']['raw_daysum'], False)