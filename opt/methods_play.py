import sys
import pathlib as pl

# Add custom modules path to sys.path and import
module_dir = pl.Path("__file__").resolve().parent

if sys.path[0] != str(module_dir):
    sys.path.insert(0, str(module_dir))

from modules.user import user
from modules.scrapedata import Webscraper
#################################################################

my_user = user()


Webscraper(my_user).stromnetz_setup(my_user.csv_dl_daysum)

