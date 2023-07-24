import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import login_details

# user input
folder = "/home/c/Downloads/csv"    # download folder for csv files
username = login_details.username   # import user credentials
password = login_details.password
start_date = '01-02-2023'           # set start date for data, format: dd-mm-yyyy
end_date = '01-03-2023'             # set end date for data, format: dd-mm-yyyy

def ff_options(dl_folder):
    ''' 
    set options for firefox webdriver 
    dl_folder: target download directory
    '''
    profile = Options()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", dl_folder)
    return profile

def date_selector(date):
    '''
    set date for csv file
    input dateformat 'dd', 'mm', 'yyyy'
    '''
    actions = ActionChains(driver)
    actions.send_keys(date[3:5]) #month
    actions.send_keys(date[:2]) #day
    actions.send_keys(date[6:])
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.perform()

def stromnetz_setup(dl_folder):
    '''
    login to stromnetz graz webportal and setup data page
    '''
    global driver
    driver = webdriver.Firefox(options=ff_options(dl_folder))
    driver.get('https://webportal.stromnetz-graz.at/login')
    driver.maximize_window()

    ##### login #####
    driver.find_element(By.NAME, "email").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH,"/html/body/div/app-root/main/div/app-login/div[2]/div[1]/form/div[3]/button").click()
    time.sleep(2)
    # go to data page
    driver.find_element(By.XPATH,"/html/body/div/app-root/main/div/app-dashboard/div[2]/div/div[1]/div[1]/div").click()
    time.sleep(2)
    # set units to [Wh]
    units_btn = driver.find_element(By.XPATH,"/html/body/div/app-root/main/div/app-overview/div/div[2]/div[3]/app-unit-selector/div/div[2]")
    units_btn.click()

def stromnetz_fillTageswerte(start, end):
    '''
    for daily average computation
    set start and end dates
    '''
    tageswerte_btn = driver.find_element(By.XPATH,"/html/body/div/app-root/main/div/app-overview/div/app-period-selector/div[1]/div/div[5]/div")
    tageswerte_btn.click()
    start_picker = driver.find_element(By.ID, "fromDayOverviewDate")
    start_picker.click()
    date_selector(start) # start date
    date_selector(end) # end date
    time.sleep(2)
    
def stromnetz_download():
    '''
    confirm dates and start download
    '''
    confirm_btn = driver.find_element(By.XPATH, '/html/body/div/app-root/main/div/app-overview/div/app-period-selector/div[2]/div/div/div/div[2]/div[2]/div[2]/button')
    download_btn = driver.find_element(By.XPATH, '/html/body/div/app-root/main/div/app-overview/reports-nav/app-header-nav/nav/div/div/div/div/div[2]/div/div[3]/div/div[2]/span')
    confirm_btn.click()
    download_btn.click()
    
stromnetz_setup(folder)
stromnetz_fillTageswerte(start_date, end_date)
stromnetz_download()
