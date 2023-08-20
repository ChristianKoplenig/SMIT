import sys
import pathlib as pl

# Add custom modules path to sys.path and import
module_dir = pl.Path("__file__").resolve().parent

if sys.path[0] != str(module_dir):
    sys.path.insert(0, str(module_dir))

from modules.user import user
#from modules.scrapedata import Webscraper
#from modules.passwordhandling import UiTools
from modules.filehandling import TomlTools
#################################################################


#Webscraper(my_user).stromnetz_setup(my_user.csv_dl_daysum)
#UiTools(my_user).pwd_dialog()

############ tomlkit #########################
a = user()
toml_filename = pl.Path(a.user_data_path)
pwd = "pwd variable"

# load
ui_data = TomlTools(a).load_toml_file(toml_filename)
print('ui_data: ' + str(ui_data))
print('before: ' + str(ui_data['Login']))

# append pwd
TomlTools(a).toml_append_password(ui_data, pwd)
print('after: ' + str(ui_data['Login']))

# write to disc
TomlTools(a).save_toml_file(toml_filename, ui_data)

print(ui_data['Login']['password'])