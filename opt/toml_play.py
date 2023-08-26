import sys
import pathlib as pl
import tomlkit

# Add custom modules path to sys.path and import
module_dir = pl.Path("__file__").resolve().parent

if sys.path[0] != str(module_dir):
    sys.path.insert(0, str(module_dir))

from SMIT.user import user

#print(tomlkit.__version__)
#########################
# tomlkit                   0.11.1           py39h06a4308_0 
#########################

class TomlTools():
    """Class for handling toml files
        Attributes
        ----------
        user : class instance
            Holds user information      
        
        Methods
        -------
        load_toml_file():
            Return toml object from filesystem.
        save_toml_file():
            Write toml object to filesystem. 
    
    """
    def __init__(self, user: user) -> None:
        self.user = user
        self.user_data = pl.Path(self.user.user_data_path)
        
    def load_toml_file(self, filename: pl.Path) -> tomlkit:
        """Read `filename` file and return TOML object.

        Parameters
        ----------
        filename : pl.Path
            Path object to the `.toml` file.

        Returns
        -------
        object
            TOML object
        """
        with open(filename, mode='rt', encoding='utf-8') as file:
            data = tomlkit.load(file)
            print('type: ' + str(type(data)))
            print(data['Login']['username'])
        
        return data    
    
    def save_toml_file(self, filename: pl.Path, toml_object: tomlkit) -> None:
        """Takes python toml object and writes `.toml` file to filesystem

        Parameters
        ----------
        filename : pl.Path
            Path to output file on filesystem
        toml_object : tomlkit
            Python TOML object
        """
        with open(filename, mode='wt', encoding='utf-8') as file:
            tomlkit.dump(toml_object, file)

    def toml_append_password(self, toml_object: tomlkit, pwd: str) -> None:
        """Append password entry und Login table.

        Parameters
        ----------
        toml_object : tomlkit
            Python TOML object.
        pwd : str
            Password for webscraping login
        """
        toml_object['Login'].add("password", pwd) # pylint: disable=no-member
        toml_object['Login']['password'].comment('Input from Password Dialog')
######## run ##################
a = user()
toml_filename = pl.Path(a.user_data_path)

ui_data = TomlTools(a).load_toml_file(toml_filename)
print('ui_data: ' + str(ui_data))
print('before: ' + str(ui_data['Login']))

pwd = "pwd variable"
# ui_data['Login'].add("password", pwd) # pylint: disable=no-member
# ui_data['Login']['password'].comment('Automatic add')

TomlTools(a).toml_append_password(ui_data, pwd)
print('after: ' + str(ui_data['Login']))

TomlTools(a).save_toml_file(toml_filename, ui_data)

print(ui_data['Login']['password'])