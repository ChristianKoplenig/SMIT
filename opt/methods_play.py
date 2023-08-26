import sys
import pathlib as pl

# Add custom modules path to sys.path and import
module_dir = pl.Path("__file__").resolve().parent

if sys.path[0] != str(module_dir):
    sys.path.insert(0, str(module_dir))

from SMIT.user import user
from SMIT.scrapedata import Webscraper
from SMIT.userinput import UiTools
from SMIT.filehandling import TomlTools
#################################################################

user = user()
scrape = Webscraper(user)
ui = UiTools(user)
toml = TomlTools(user)

# User Variables
#print(vars(user))
#print(user.Login['username'])

# Test Login
def test_login():
    scrape.stromnetz_setup(user.Folder['raw_daysum'])
    print(user.Folder['raw_daysum'])
#test_login()


# Tomlkit
def load_toml_file():
    toml_filename = pl.Path(user.Path['user_data'])
    user_data = toml.load_toml_file(toml_filename)
    print('ui_data: ' + str(user_data))
    return user_data
