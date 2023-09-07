"""Docstring for scrape test
"""
# pylint: disable=no-member
import pytest # pylint: disable=import-error

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

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
                          log_output=app.Path['webdriver_logFolder'])
    driver = webdriver.Firefox(options=profile, service=service)
    
    driver.get('https://github.com')
    
    mail_element_xpath = '//*[@id="user_email"]'
    loaded_mail_element = driver.find_element(By.XPATH, mail_element_xpath)
    
    assert loaded_mail_element.is_displayed()
