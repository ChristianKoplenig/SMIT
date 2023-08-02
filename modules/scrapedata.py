'''
Tools for scraping data from website
'''
import time
from datetime import date, timedelta
import os.path
# Webdriver imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Custom imports
from modules import dynamicclass
from modules import filepersistence

# create user
User = dynamicclass.create_user()

def wait_and_click(elementXpath):
    '''
    waits until an web element is clickable (longest 10s) and clicks on element
    elementXpath format: 'XPATH', parentesis important 
    '''
    switchName = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, elementXpath))
    )
    switchName.click()   
        
def ff_options(dl_folder, headless: bool = False):
    ''' 
    set options for firefox webdriver 
    dl_folder: target download directory for firefox
    headless: activate firefox headless mode
    '''
    dl_path = os.path.abspath(dl_folder) # convert relative download path to absolute path
    profile = Options()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.alwaysOpenPanel", False)
    profile.set_preference("browser.download.dir", dl_path)
    profile.set_preference('webdriver.log.init', True)
    
    if headless is True:
        profile.add_argument("-headless")
        print('Firefox headless mode activated')
    
    return profile

def start_date_updater(dates):
    '''
    update start/end date for autofill
    run AFTER download routine
    '''   
    if dates['last_scrape'] == 'never':                                                                         # update dates after first run
        dates['start'] = date.today().strftime('%d-%m-%Y')
    
    if not dates['last_scrape'] == 'never' and not dates['last_scrape'] == date.today().strftime('%d-%m-%Y'):   # update start/end dates
        dates['start'] = dates['last_scrape']
    
    dates['last_scrape'] = date.today().strftime('%d-%m-%Y')                                                    # update scraper log
    dates['start'] = date.today().strftime('%d-%m-%Y')                                                          # update scraper log
    
    filepersistence.save_dates_loggingFile(dates)

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

def stromnetz_setup(dl_folder, headless):
    '''
    login to stromnetz graz webportal and setup data page
    '''
    global driver
    service = Service(log_path=User.webdriver_logFolder)    
    driver = webdriver.Firefox(options=ff_options(dl_folder, headless), service=service)
    driver.get(User.login_url)
    driver.maximize_window()

    ##### login #####
    driver.find_element(By.NAME, "email").send_keys(User.username)
    driver.find_element(By.NAME, "password").send_keys(User.password)
    wait_and_click('/html/body/div/app-root/main/div/app-login/div[2]/div[1]/form/div[3]/button')                       # login confirmation
    wait_and_click('/html/body/div/app-root/main/div/app-dashboard/div[2]/div/div[1]/div[1]/div')                       # open data page
    wait_and_click('/html/body/div/app-root/main/div/app-overview/div/div[2]/div[3]/app-unit-selector/div/div[2]')      # set unit to [Wh]

def stromnetz_fillTageswerte(start, end):
    '''
    for daily average computation
    set start and end dates
    '''
    wait_and_click('/html/body/div/app-root/main/div/app-overview/div/app-period-selector/div[1]/div/div[5]/div')                           # select daily sum measurements
    wait_and_click('//*[@id="fromDayOverviewDate"]')                                                                                        # set cursor in start date input field
    date_selector(start)    # start date
    date_selector(end)      # end date
    wait_and_click('/html/body/div/app-root/main/div/app-overview/div/app-period-selector/div[2]/div/div/div/div[2]/div[2]/div[2]/button')  # confirm date selections

    time.sleep(3) # wait for element to load

def stromnetz_download():
    '''
    start download of csv file
    '''
    wait_and_click('/html/body/div/app-root/main/div/app-overview/reports-nav/app-header-nav/nav/div/div/div/div/div[2]/div/div[3]/div/div[2]/span')

def day_night_selector(day_night):
    '''
    switch between day and night meassurements
    day_night: values 'day' / 'night', defaults to day
    '''
    wait_and_click('/html/body/div/app-root/main/div/app-overview/reports-nav/app-meter-point-selector/div/div[2]/div/div[2]/ul/li/a')              # make dropdown active
    
    if day_night == 'night':
        wait_and_click('/html/body/div/app-root/main/div/app-overview/reports-nav/app-meter-point-selector/div/div[2]/div/div[2]/ul/li/ul/li[2]/a') # choose night measurements
    else:
        wait_and_click('/html/body/div/app-root/main/div/app-overview/reports-nav/app-meter-point-selector/div/div[2]/div/div[2]/ul/li/ul/li[1]/a') # choose day measurements
    
    time.sleep(3)
    
################ run #######################  
def get_daysum_files(headless: bool=False): 
    '''
    download csv files for day and night measurements
    ''' 
    filepersistence.initialize_dates_log()
    dates = filepersistence.create_dates_var()
    dates['end'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')      # set end date for scraping to yesterday
        
    if not dates['start'] == date.today().strftime('%d-%m-%Y'):                 # scrape just once a day
        stromnetz_setup(User.csv_dl_daysum, headless)
        day_night_selector('night')
        stromnetz_fillTageswerte(dates['start'], dates['end'])
        stromnetz_download()
        day_night_selector('day')
        stromnetz_fillTageswerte(dates['start'], dates['end'])
        stromnetz_download()
        print('Downloaded data with the following arguments:')
        print('Start date: ' + dates['start'])
        print('End date: ' + dates['end'])
        start_date_updater(dates)
