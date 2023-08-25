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

# Test the webdriver integration
def test_webdriver() -> None:
    """Open firefox instance with webdriver
    No data from custom modules
    """
    from selenium import webdriver
    from selenium.webdriver.firefox.service import Service
    option = webdriver.FirefoxOptions()
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    driverService = Service(executable_path='/snap/bin/geckodriver')
    driver = webdriver.Firefox(service=driverService, options=option)
    driver.get("https://www.google.com")
    
# Test Login to stromnetz graz website
def sng_login():
    """Login to sng data page with headless mode off.
    """
    from modules.scrapedata import Webscraper
    scrape = Webscraper(user)
    scrape.stromnetz_setup(user.Folder['raw_daysum'], False)
sng_login()
    
# Test Tomlkit
def load_toml_file() -> 'ClassType':
    """Opens `user_data.toml` file

    Returns
    -------
    Class
        TOMLDokument with user data
    """
    from modules.filehandling import TomlTools
    toml = TomlTools(user)
    toml_filename = pl.Path(user.Path['user_data'])
    user_data = toml.load_toml_file(toml_filename)
    print('ui_data: ' + str(user_data) + '\n')
    print(type(user_data))
    return user_data

# Test GUI
def password_dialog() -> None:
    """Starts the 'Input Password' routine
    WARNING: Changes affect the `user_data` attributes and 
            `user_data.toml` file
    """
    from modules.userinput import UiTools
    ui = UiTools(user)
    ui.password_dialog()
    
# Test crypto
def test_rsa() -> None:
    """Test rsa encrypt/decrypt workflow.
    """
    from modules.rsahandling import RsaTools
    rsa = RsaTools(user)
    test_pwd = 'String to test Rsa functionality'
    print('#### Input ####')
    print('Unmodified input: ' + '\n' + str(test_pwd) + '\n')
    print('Type: ' + str(type(test_pwd)) + '\n')
    pwd_enc = rsa.encrypt_pwd(test_pwd)
    print('#### Encryption ####')
    print('Enrypted pwd: ' + '\n' + str(pwd_enc) + '\n')
    print('Type: ' + str(type(pwd_enc)) + '\n')
    pwd_dec = rsa.decrypt_pwd(pwd_enc)
    print('#### Dencryption ####')
    print('Decrypted pwd: ' + '\n' + str(pwd_dec) + '\n')
    print('Type: ' + str(type(pwd_dec)) + '\n')