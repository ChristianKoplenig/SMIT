from selenium import webdriver
from selenium.webdriver.common.by import By
import login_details
import time

username = login_details.username
password = login_details.password

driver = webdriver.Firefox()
driver.get('https://webportal.stromnetz-graz.at/login')

# Login
driver.find_element(By.NAME, "email").send_keys(username)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.XPATH,"/html/body/div/app-root/main/div/app-login/div[2]/div[1]/form/div[3]/button").click()
# wait for home webpage loading
time.sleep(5)

# click for analysis webpage
driver.find_element(By.XPATH,"/html/body/div/app-root/main/div/app-dashboard/div[2]/div/div[1]/div[1]/div").click()
