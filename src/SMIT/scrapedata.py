"""Selenium Webscraper

---
`Webscraper`
------------

- Configure Firefox
- Manage scrape dates
- Download data

Typical usage:

    app = Application()
    app.scrape.method()
"""
import time
from datetime import date, timedelta
import pathlib as pl
# Type hints
from typing import TYPE_CHECKING
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
# Import just for type hints
if TYPE_CHECKING:
    from SMIT.application import Application


class Webscraper():
    """Interact with selenium webdriver library.
    
    ---
    
    Configure Firefox webdriver, set all paths for downloading
    the `.csv` files, retrieve the stored password,
    manage the dates for downloading files and download files
    for day and night meter. 

    Attributes:
        app (class): Accepts `SMIT.application.Application` type attribute.
    """
    def __init__(self, app: 'Application') -> None:

        self.user = app
        self.driver = None
        self.logger = app.logger
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)

    def wait_and_click(self, elementXpath: str) -> None:
        """Wait for web element and trigger action.

        As soon as the element is
        available it's action will be triggered.
        
        Note:
        
            Helper function.  
            The timeout for the element to be available is
            set to 10s. After this a exception is triggered.

        Args:
            elementXpath (string): String formatted `xpath` of 
                                    the element to click on.
        """
        switchName = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, elementXpath))
        )
        switchName.click()

    def _ff_options(self, dl_folder: str,
                    headless: bool) -> webdriver.FirefoxOptions:
        """Set options for Firefox webdriver.

        Set firefox to start download in background,
        set the path to the download folder, 
        set the log directory and configure headless mode.
        
        Args:
            dl_folder (string): Target download directory
                                for Firefox webdriver.
            headless (bool = False): Run Firefox in headless mode.

        Returns
        -------
        webdriver.FirefoxOptions
            Options for Firefox webdriver instance.
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
            self.logger.info('Firefox headless mode activated')

        return profile

    def start_date_updater(self, dates: dict) -> None:
        """Scrape dates management.
        
        After initial run set start date for next run.  
        On each consecutive run set last_scrape date 
        and start date to the date of the last run. 

        Info:
            Run AFTER download routine.

        Args:
            dates (dict): Object for scrape date management.
        """
        # Update dates after first run
        if dates['last_scrape'] == 'never':
            dates['start'] = date.today().strftime('%d-%m-%Y')
        # Update start/end dates
        if not dates['last_scrape'] == 'never' and not dates['last_scrape'] == date.today().strftime('%d-%m-%Y'):
            dates['start'] = dates['last_scrape']

        dates['last_scrape'] = date.today().strftime('%d-%m-%Y')
        dates['start'] = date.today().strftime('%d-%m-%Y')

        self.user.persistence.save_dates_log(dates)

    def _decode_password(self) -> str:
        """Read and decode stored password.

        If a password is stored in `user_data.toml`
        the password will be read, the bytes object will
        be decoded and the rsa encryption will be decrypted.
        
        Note:
            __The password will be send in plain text.__  
            Due to the usage of a webscraper I don't know
            a alternative to sending the password in plain text.

        Returns:
            string: Decoded plain text password string.
        """
        # Read encoded password
        pwd_enc = self.user.Login['password']
        # Decode the base64 conversion
        b64_decode = base64.b64decode(pwd_enc)
        # Decrypt rsa encryption
        password = self.user.rsa.decrypt_pwd(b64_decode)
        return password

    def sng_login(self, dl_folder: pl.Path,
                  headless: bool = False) -> None:
        """Login to "Stromnetz Graz" web portal and setup data page.

        Initialize Firefox webdriver.  
        Send username and password to the login page.  
        Open the data page and set units for data 
        processing to [Wh].
         
        Args:
            dl_folder (pathlib.Path): Target download directory 
                                        for Firefox webdriver.
            headless (bool = False): Firefox headless mode option.
        """
        service = Service(executable_path=self.user.Path['geckodriver_executable'],
                          log_output=self.user.Path['webdriver_logFolder'])
        self.driver = webdriver.Firefox(options=self._ff_options(dl_folder, headless),
                                        service=service)
        # Load Url
        self.driver.get(self.user.Login['url'])
        self.driver.maximize_window()
        # Send username and password
        self.driver.find_element(By.NAME, "email").send_keys(self.user.Login['username'])
        self.driver.find_element(By.NAME, "password").send_keys(self._decode_password())
        # Login confirmation
        self.wait_and_click('/html/body/div/app-root/main/div/app-login/div[2]/div[1]/form/div[3]/button')
        # Open data page
        self.wait_and_click('/html/body/div/app-root/main/div/app-dashboard/div[2]/div/div[1]/div[1]/div')
        # Set unit to [Wh]
        self.wait_and_click('/html/body/div/app-root/main/div/app-overview/div/div[2]/div[3]/app-unit-selector/div/div[2]')
        self.logger.debug('Login to Stromnetz Graz successful')

    def _sng_input_dates(self, input_date: str) -> None:
        """Pass dates to web form.

        Fill dates and click through the data page web form.
        
        Note:
            Depending on the OS setup different day/month
            sequences have to be sent. This is handled in 
            the function.

        Args:
            input_date (string): Date with format dd-mm-yyyy
        """
        language = self.driver.execute_script("return navigator.language;")
        actions = ActionChains(self.driver)

        if language == 'de':
            actions.send_keys(input_date[ :2])  # Day
            actions.send_keys(input_date[3:5])  # Month
        else:
            actions.send_keys(input_date[3:5])  # Month
            actions.send_keys(input_date[ :2])  # Day
        actions.send_keys(input_date[6:])
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.perform()

    def _sng_fill_dates_element(self, start: str, end: str) -> None:
        """Activate daily average computation and fill dates.
        
        Activate the web element for daily average data.  
        Call `SMIT.scrapedata.Webscraper._sng_input_dates`
        method and confirm the selected dates.  
        Wait for data to be loaded.

        Args:
            start (string): Date with format dd-mm-yyyy
            end (string): Date with format dd-mm-yyyy
        """
        # Select daily sum measurements
        self.wait_and_click('/html/body/div/app-root/main/div/app-overview/div/app-period-selector/div[1]/div/div[5]/div')
        # Set cursor in start date input field
        self.wait_and_click('//*[@id="fromDayOverviewDate"]')
        self._sng_input_dates(start)    # Start date
        self._sng_input_dates(end)      # End date
        # Confirm date selections
        self.wait_and_click('/html/body/div/app-root/main/div/app-overview/div/app-period-selector/div[2]/div/div/div/div[2]/div[2]/div[2]/button')

        time.sleep(3)   # Wait for element to load

    def _sng_start_download(self) -> None:
        """Click download button.
        
        Start downloading files with filled dates from scraper.
        """
        self.wait_and_click('/html/body/div/app-root/main/div/app-overview/reports-nav/app-header-nav/nav/div/div/div/div/div[2]/div/div[3]/div/div[2]/span')

    def _sng_switch_day_night_meassurements(self, day_night: str) -> None:
        """Select meter for data setup.

        Choose between day and night meter in pulldown menu.
        The selected meter defines which data set is downloaded.
        
        Note:
            Defaults to day meassurements.

        Args:
            day_night (string): Accepts 'day' or 'night'.
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

    def get_daysum_files(self, headless: bool = False) -> None:
        """Initiate download for daily average data.
        
        - Manage scrape dates logging.
        - Set Firefox headless mode according to config.
        - Download files for day and night meter.
        
        Args:
            headless (bool = False): Firefox headless mode option.
        """
        self.user.persistence.initialize_dates_log()
        dates = self.user.persistence.load_dates_log()
        dates['end'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')

        # scrape just once a day
        if not dates['start'] == date.today().strftime('%d-%m-%Y'):
            self.sng_login(self.user.Folder['raw_daysum'], headless)
            self._sng_switch_day_night_meassurements('night')
            self._sng_fill_dates_element(dates['start'], dates['end'])
            self._sng_start_download()
            self._sng_switch_day_night_meassurements('day')
            self._sng_fill_dates_element(dates['start'], dates['end'])
            self._sng_start_download()
            self.logger.info('Downloaded data with the following arguments:')
            self.logger.info('Start date: ' + dates['start'])
            self.logger.info('End date: ' + dates['end'])
            self.start_date_updater(dates)

    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"


# Pdoc config get underscore methods
__pdoc__ = {name: True
            for name, classes in globals().items()
            if name.startswith('_') and isinstance(classes, type)}


__pdoc__.update({f'{name}.{member}': True
                 for name, classes in globals().items()
                 if isinstance(classes, type)
                 for member in classes.__dict__.keys()
                 if member not in {'__module__', '__dict__',
                                   '__weakref__', '__doc__'}})

__pdoc__.update({f'{name}.{member}': False
                 for name, classes in globals().items()
                 if isinstance(classes, type)
                 for member in classes.__dict__.keys()
                 if member.__contains__('__') and member not in {'__module__', '__dict__',
                                                                 '__weakref__', '__doc__'}})
