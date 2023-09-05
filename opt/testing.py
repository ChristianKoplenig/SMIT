"""
Collection of usefull snipets 
"""
# pylint: disable=no-member
# pylint: disable=import-outside-toplevel
import pathlib as pl

# Setup
from SMIT.application import Application
user = Application(True)
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
    from SMIT.scrapedata import Webscraper
    scrape = Webscraper(user)
    scrape.sng_login(user.Folder['raw_daysum'], False)
    
# Test Tomlkit
def load_toml_file() -> 'ClassType':
    """Opens `user_data.toml` file

    Returns
    -------
    Class
        TOMLDokument with user data
    """
    from SMIT.filehandling import TomlTools
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
    #from SMIT.userinput import UiTools
    ui = user.gui
    ui.password_dialog()
    #print(vars(ui))
       
# Test crypto
def test_rsa() -> None:
    """Test rsa encrypt/decrypt workflow.
    """
    #from SMIT.rsahandling import RsaTools
    #rsa = RsaTools(user)
    test_pwd = 'String to test Rsa functionality'
    print('#### Input ####')
    print('Unmodified input: ' + '\n' + str(test_pwd) + '\n')
    print('Type: ' + str(type(test_pwd)) + '\n')
    pwd_enc = user.rsa.encrypt_pwd(test_pwd)
    print('#### Encryption ####')
    print('Enrypted pwd: ' + '\n' + str(pwd_enc) + '\n')
    print('Type: ' + str(type(pwd_enc)) + '\n')
    pwd_dec = user.rsa.decrypt_pwd(pwd_enc)
    print('#### Decryption ####')
    print('Decrypted pwd: ' + '\n' + str(pwd_dec) + '\n')
    print('Type: ' + str(type(pwd_dec)) + '\n')

# Test logging
def test_logging() -> None:
    """Generate a test log entry 
    """
    user.logger.debug('Logging test sucessfull')
    
############## load test #######################
password_dialog()
#test_logging()
#test_rsa()
################################################
#print(f"User Attribute: {user.Login['password']}")