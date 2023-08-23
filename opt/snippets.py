"""
Collection of usefull snipets 
"""
# Imports to make custom modules work
import sys
import pathlib as pl

# Add custom modules path to sys.path and import
module_dir = pl.Path("__file__").resolve().parent

if sys.path[0] != str(module_dir):
    sys.path.insert(0, str(module_dir))
################################################
# Setup
from modules.user import user
user = user() 
################################################
def sng_login():
    """Login to sng data page with headless mode off.
    """
    from modules.scrapedata import Webscraper
    Webscraper(user).stromnetz_setup(user.Folder['raw_daysum'], False)