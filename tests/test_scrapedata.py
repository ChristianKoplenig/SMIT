# pylint: disable=no-member
#import pickle
import pathlib as pl
from datetime import date,timedelta
import pytest # pylint: disable=import-error
from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from SMIT.application import Application

app = Application(True)

@pytest.mark.smoke
@pytest.mark.scraping
def test_webdriver():
    """Webdriver open site
    """
    # Set firefox options
    profile = Options()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.alwaysOpenPanel", False)
    #profile.set_preference("browser.download.dir", dl_path)
    profile.set_preference('webdriver.log.init', True)
    profile.add_argument('--no-sandbox')
    profile.add_argument('--disable-dev-shm-usage')
    profile.add_argument("-headless")
    
    
    service = Service(executable_path=app.Path['geckodriver_executable'],
                          log_path=app.Path['webdriver_logFolder'])
    driver = webdriver.Firefox(options=profile, service=service)
    
    driver.get('https://github.com')
    
    mail_element_xpath = '//*[@id="user_email"]'
    loaded_mail_element = driver.find_element(By.XPATH, mail_element_xpath)
    
    assert loaded_mail_element.is_displayed()
