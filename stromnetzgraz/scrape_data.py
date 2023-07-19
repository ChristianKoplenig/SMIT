from selenium import webdriver
from selenium.webdriver.common.by import By
import login_details

username = login_details.username
password = login_details.password

driver = webdriver.Firefox()
driver.get('https://webportal.stromnetz-graz.at/login')

driver.find_element(By.NAME, "email").send_keys(username)

# driver.get("https://www.linkedin.com/uas/login?")
# driver.maximize_window()
