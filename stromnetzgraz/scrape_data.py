import time
from datetime import date, timedelta
import pickle
import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import user_data

# If no persisted date exists, create dict for dates and use start date from user_data
if not os.path.isfile(user_data.persist_dates):
    with open('dates.pkl', 'wb') as pk:
        dates = dict()
        dates['start'] = user_data.csv_startDate                                        # set start date for initial run, format: dd-mm-yyyy
        dates['end'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')          # set end date yesterday for initial run, format: dd-mm-yyyy
        dates['last_scrape'] = 'never'                                                  # flag for first run
        pickle.dump(dates, pk)
    pk.close()

# Initialize dates variable from storage    
with open('dates.pkl', 'rb') as pk:
    dates = pickle.load(pk)  

##### useful functions #####
def wait_and_click(elementXpath):
    switchName = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, elementXpath))
    )
    switchName.click()
###############        
        
def ff_options(dl_folder):
    ''' 
    set options for firefox webdriver 
    dl_folder: target download directory for firefox
    '''
    profile = Options()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", dl_folder)
    return profile

def date_updater():
    '''
    update start/end date for autofill
    '''
    global dates
    if not (dates['last_scrape'] == (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')):       # check if yesterdays date already in log
        dates['last_scrape'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
    
    if not dates['last_scrape'] == 'never':                                                         # update dates after first run
        dates['start'] = dates['last_scrape']
        dates['end'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
    
    with open('dates.pkl', 'wb') as pk:                                                             # save logfile
        pickle.dump(dates, pk)
    pk.close()

def date_selector(input_date):
    '''
    set date for csv file
    input dateformat 'dd-mm-yyyy'
    '''
    actions = ActionChains(driver)
    actions.send_keys(input_date[3:5]) #month
    actions.send_keys(input_date[:2]) #day
    actions.send_keys(input_date[6:])
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.perform()

def stromnetz_setup(dl_folder):
    '''
    login to stromnetz graz webportal and setup data page
    '''
    global driver
    driver = webdriver.Firefox(options=ff_options(dl_folder))
    driver.get(user_data.login_url)
    driver.maximize_window()

    ##### login #####
    driver.find_element(By.NAME, "email").send_keys(user_data.username)
    driver.find_element(By.NAME, "password").send_keys(user_data.password)
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
    date_selector(start)    # start date
    date_selector(end)      # end date
    confirm_btn = driver.find_element(By.XPATH, '/html/body/div/app-root/main/div/app-overview/div/app-period-selector/div[2]/div/div/div/div[2]/div[2]/div[2]/button')
    confirm_btn.click()
    time.sleep(2)           # wait for data load
    
def stromnetz_download():
    '''
    start download of csv file
    '''
    download_btn = driver.find_element(By.XPATH, '/html/body/div/app-root/main/div/app-overview/reports-nav/app-header-nav/nav/div/div/div/div/div[2]/div/div[3]/div/div[2]/span')
    download_btn.click()

def day_night_selector(day_night):
    '''
    switch between day and night meassurements
    day_night: values 'day' / 'night', defaults to day
    '''
    dn_switch = driver.find_element(By.XPATH, '/html/body/div/app-root/main/div/app-overview/reports-nav/app-meter-point-selector/div/div[2]/div/div[2]/ul/li/a')  
    dn_switch.click()
    
    if day_night == 'night':
        wait_and_click('/html/body/div/app-root/main/div/app-overview/reports-nav/app-meter-point-selector/div/div[2]/div/div[2]/ul/li/ul/li[2]/a')
    else:
        wait_and_click('/html/body/div/app-root/main/div/app-overview/reports-nav/app-meter-point-selector/div/div[2]/div/div[2]/ul/li/ul/li[1]/a')    
    
################ run #######################    
stromnetz_setup(user_data.csv_dlFolder)
time.sleep(3)
day_night_selector('day')
#stromnetz_fillTageswerte(dates['start'], dates['end'])
#date_updater()