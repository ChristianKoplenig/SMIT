"""
Tools for scraping data from website
"""
import time
from datetime import date, timedelta
import pathlib as pl
# Password handling
import base64
# Webdriver imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Custom modules
#from SMIT.filepersistence import Persistence
#from SMIT.rsahandling import RsaTools

class Webscraper():
    """Methods for interacting with webdriver module
        
        Attributes
        ----------
        user : class instance
            Holds user information      
        
        Methods
        -------
        wait_and_click(elementXpath):
            Wait for web element and click.
        ff_options(dl_folder, headless):
            Set options for firefox webdriver.
        start_date_updater(dates):
            Update runtime dates in dates dict.
        date_selector(input_date):
            Fill dates in date-input web element.
        stromnetz_setup(dl_folder, headless):
            Login to stromnetz graz webportal and setup data page.
        stromnetz_FillTageswerte(start, end):
            Activate day sum web-element and fill start/end dates.
        stromnetz_download():
            Start download from webpage.
        day_night_selector(day_night):
            Switch between day/night meter.
        get_daysum_files(headless):
            Download data summarized by day.
        decode_password():
            Decode password from user instance and return plain text string.
    """
    def __init__(self, user: 'user') -> None:
        """Initialize Class with all attributes from `UserClass`

        Parameters
        ----------
        user : class instance
            User data initiated via `user()` function from user module            
        """        
        self.user = user
            
    def wait_and_click(self, elementXpath: str) -> None:
        """Wait for web element and click.

        Timeout 10s.

        Parameters
        ----------
        elementXpath : XPATH
            `xpath` of the element to click on
        """
        switchName = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, elementXpath))
        )
        switchName.click()   

    def ff_options(self, dl_folder: str, headless: bool = False) -> webdriver.FirefoxOptions:
        """Set options for firefox webdriver.

        Parameters
        ----------
        dl_folder : folder path
            Target donwload directory for Firefox webdriver.
        headless : bool, optional
            activate Firefox headless mode, by default False

        Returns
        -------
        webdriver profile
            Options for Firefox webdriver.
        """
        # Set path variables
        dl_path = str(pl.Path(dl_folder).absolute())
        
        # Set firefox options
        profile = Options()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.alwaysOpenPanel", False)
        profile.set_preference("browser.download.dir", dl_path)
        profile.set_preference('webdriver.log.init', True)
        profile.add_argument('--no-sandbox')
        profile.add_argument('--disable-dev-shm-usage')

        if headless is True:
            profile.add_argument("-headless")
            print('Firefox headless mode activated')

        return profile

    def start_date_updater(self, dates: dict) -> None:
        """Update runtime dates in dates dict.

        Run AFTER download routine

        Parameters
        ----------
        dates : dict
            Dict with parameters for date management
        """
        # update dates after first run
        if dates['last_scrape'] == 'never':                                                                         
            dates['start'] = date.today().strftime('%d-%m-%Y')
        # update start/end dates
        if not dates['last_scrape'] == 'never' and not dates['last_scrape'] == date.today().strftime('%d-%m-%Y'):   
            dates['start'] = dates['last_scrape']

        dates['last_scrape'] = date.today().strftime('%d-%m-%Y')
        dates['start'] = date.today().strftime('%d-%m-%Y')

        self.user.persistence.save_dates_loggingFile(dates)

    def decode_password(self) -> str:
        """Get encoded password return decoded password.
        
        The password will be send in plain text.
        At the moment I see no other option.

        Parameters
        ----------
        pwd_string : str
            Encoded password 

        Returns
        -------
        str
            Decoded plain text password string
        """
        # Read encoded password 
        pwd_enc = self.user.Login['password']
        # Decode the base64 conversion
        b64_decode = base64.b64decode(pwd_enc)
        # Decrypt rsa encryption
        #password = RsaTools(self.user).decrypt_pwd(b64_decode)
        password = self.user.rsa.decrypt_pwd(b64_decode)
        return password
           
    def stromnetz_setup(self, dl_folder: pl.Path, headless: bool=False) -> None:
        """Login to stromnetz graz webportal and setup data page.

        Parameters
        ----------
        dl_folder : folder path
            Target donwload directory for Firefox webdriver.
        headless : bool, optional
            activate Firefox headless mode, by default False
        """
        global driver
        
        service = Service(executable_path= self.user.Path['geckodriver_executable'], log_path= self.user.Path['webdriver_logFolder'])
        driver = webdriver.Firefox(options=self.ff_options(dl_folder, headless), service=service)
        driver.get(self.user.Login['url'])
        driver.maximize_window()

        ##### login #####
        driver.find_element(By.NAME, "email").send_keys(self.user.Login['username'])
        driver.find_element(By.NAME, "password").send_keys(self.decode_password())
        # login confirmation
        self.wait_and_click('/html/body/div/app-root/main/div/app-login/div[2]/div[1]/form/div[3]/button')
        # open data page                       
        self.wait_and_click('/html/body/div/app-root/main/div/app-dashboard/div[2]/div/div[1]/div[1]/div')
        # set unit to [Wh]                       
        self.wait_and_click('/html/body/div/app-root/main/div/app-overview/div/div[2]/div[3]/app-unit-selector/div/div[2]')      

    def date_selector(self, input_date: str) -> None:
        """Fill dates in date-input web element.

        Parameters
        ----------
        input_date : string
            Date with format dd-mm-yyyy
        """
        language = driver.execute_script("return navigator.language;")
        actions = ActionChains(driver)
        
        if language == 'de':
            actions.send_keys(input_date[ :2]) #day
            actions.send_keys(input_date[3:5]) #month
        else:
            actions.send_keys(input_date[3:5]) #month
            actions.send_keys(input_date[ :2]) #day
        actions.send_keys(input_date[6:])
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.perform()
    
    def stromnetz_fillTageswerte(self, start: str, end: str) -> None:
        """Activate day sum web-element and fill start/end dates.

        Parameters
        ----------
        start : string
            Date with format dd-mm-yyyy
        end : string
            Date with format dd-mm-yyyy
        """
        # select daily sum measurements
        self.wait_and_click('/html/body/div/app-root/main/div/app-overview/div/app-period-selector/div[1]/div/div[5]/div')
        # set cursor in start date input field                           
        self.wait_and_click('//*[@id="fromDayOverviewDate"]')                                                                                        
        self.date_selector(start)    # start date
        self.date_selector(end)      # end date
        # confirm date selections
        self.wait_and_click('/html/body/div/app-root/main/div/app-overview/div/app-period-selector/div[2]/div/div/div/div[2]/div[2]/div[2]/button')  

        time.sleep(3) # wait for element to load

    def stromnetz_download(self) -> None:
        """Click download button web-element.
        """
        self.wait_and_click('/html/body/div/app-root/main/div/app-overview/reports-nav/app-header-nav/nav/div/div/div/div/div[2]/div/div[3]/div/div[2]/span')

    def day_night_selector(self, day_night: str) -> None:
        """Switch between day/night meassurements.

        Defaults to day meassurements.

        Parameters
        ----------
        day_night : string
            either `day` or `night`
        """
        # make dropdown active
        self.wait_and_click('/html/body/div/app-root/main/div/app-overview/reports-nav/app-meter-point-selector/div/div[2]/div/div[2]/ul/li/a')              
        # choose night measurements
        if day_night == 'night':
            self.wait_and_click('/html/body/div/app-root/main/div/app-overview/reports-nav/app-meter-point-selector/div/div[2]/div/div[2]/ul/li/ul/li[2]/a') 
        # choose day measurements
        else:
            self.wait_and_click('/html/body/div/app-root/main/div/app-overview/reports-nav/app-meter-point-selector/div/div[2]/div/div[2]/ul/li/ul/li[1]/a') 

        time.sleep(3)
 
    def get_daysum_files(self, headless: bool=False) -> None: 
        """Initiate '.csv' files download for day sum files.

        Parameters
        ----------
        headless : bool, optional
            Run Firefox in headless mode defaults to `False`.
        """
        self.user.persistence.initialize_dates_log()
        dates = self.user.persistence.create_dates_var()
        dates['end'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
        
        # scrape just once a day
        if not dates['start'] == date.today().strftime('%d-%m-%Y'):                 
            self.stromnetz_setup(self.user.Folder['raw_daysum'], headless)
            self.day_night_selector('night')
            self.stromnetz_fillTageswerte(dates['start'], dates['end'])
            self.stromnetz_download()
            self.day_night_selector('day')
            self.stromnetz_fillTageswerte(dates['start'], dates['end'])
            self.stromnetz_download()
            print('Downloaded data with the following arguments:')
            print('Start date: ' + dates['start'])
            print('End date: ' + dates['end'])
            self.start_date_updater(dates)
        
    def __repr__(self) -> str:
        return f"Module Class {self.__class__.__name__}"
        
    def __str__(self) -> str:
        return self.user.Login['username']