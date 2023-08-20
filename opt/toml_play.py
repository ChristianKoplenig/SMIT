import sys
import pathlib as pl

# Add custom modules path to sys.path and import
module_dir = pl.Path("__file__").resolve().parent

if sys.path[0] != str(module_dir):
    sys.path.insert(0, str(module_dir))

from modules.user import user

# Toml imports
import tomlkit
if sys.version_info < (3, 11):
    import tomli as tomlib
else:
    import tomlib

#print(tomlib.__version__)
####### toml conda versions
# toml                      0.10.2             pyhd3eb1b0_0  
# tomli                     2.0.1            py39h06a4308_0  
# tomlkit                   0.11.1           py39h06a4308_0 
#########################

class TomlPlay():
    def __init__(self, user: user) -> None:
        self.user = user
        self.user_data = pl.Path(self.user.user_data_path)
        
    def load_toml(self):
        with open(self.user_data, mode='rb') as toml:
            data = tomlib.load(toml)
            print('type: ' + str(type(data)))
            print(data)
            print(data['Login']['username'])
            print(data['Login'])

a = user()            
#TomlPlay(a).load_toml()

class TomlTools():
    def __init__(self, user: user) -> None:
        self.user = user
        self.user_data = pl.Path(self.user.user_data_path)
        
    def load_tomlkit(self):
        """Loads `user_data.toml` as python toml object
        """
        with open(self.user_data, mode='rt', encoding='utf-8') as ud:
            data = tomlkit.load(ud)
            print('type: ' + str(type(data)))
            print(data['Login']['username'])
        
        return data    
    
    def save_tomlkit(self, config_file):
        """Write 'user_data.toml`
        """
        with open(self.user_data, mode='wt', encoding='utf-8') as ud:
            tomlkit.dump(config_file, ud)

ui_data = TomlTools(a).load_tomlkit()
print('ui_data: ' + str(ui_data))
print('before: ' + str(ui_data['Login']))

pwd = "as /n df  \n bla"
ui_data['Login'].add("password", pwd) # pylint: disable=no-member
ui_data['Login']['password'].comment('Automatic add')

print('after: ' + str(ui_data['Login']))

TomlTools(a).save_tomlkit(ui_data)

print(ui_data['Login']['password'])