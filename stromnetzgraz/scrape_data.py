import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import login_details

# import user credentials from file
username = login_details.username
password = login_details.password

##### open firefox instance #####
driver = webdriver.Firefox()
driver.get('https://webportal.stromnetz-graz.at/login')
driver.maximize_window()

##### login #####
driver.find_element(By.NAME, "email").send_keys(username)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.XPATH,"/html/body/div/app-root/main/div/app-login/div[2]/div[1]/form/div[3]/button").click()
# wait for loading page
time.sleep(2)
# click for analysis webpage
driver.find_element(By.XPATH,"/html/body/div/app-root/main/div/app-dashboard/div[2]/div/div[1]/div[1]/div").click()
# wait for loading page
time.sleep(2)

##### define buttons #####
tageswerte_btn = driver.find_element(By.XPATH,"/html/body/div/app-root/main/div/app-overview/div/app-period-selector/div[1]/div/div[5]/div")
units_btn = driver.find_element(By.XPATH,"/html/body/div/app-root/main/div/app-overview/div/div[2]/div[3]/app-unit-selector/div/div[2]")
tageswerte_btn.click()
units_btn.click()
start_picker = driver.find_element(By.ID, "fromDayOverviewDate")
end_picker = driver.find_element(By.ID, 'toDayOverviewDate')
confirm_btn = driver.find_element(By.XPATH, '/html/body/div/app-root/main/div/app-overview/div/app-period-selector/div[2]/div/div/div/div[2]/div[2]/div[2]/button')
werte_btn = driver.find_element(By.XPATH, '/html/body/div/app-root/main/div/app-overview/div/div[2]/div[1]/div/div[1]')

##### setup for export #####
actions = ActionChains(driver)
start_picker.click()

# date selection
def date_selector(day, month, year):
    '''
    set start date for csv file
    input dateformat 'dd', 'mm', 'yyyy'
    '''
    actions.send_keys(month) #month
    actions.send_keys(day) #day
    actions.send_keys(year)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.perform()


date_selector('01', '02', '2023') # start date
date_selector('03', '04', '2023') # end date
confirm_btn.click()
werte_btn.click()
