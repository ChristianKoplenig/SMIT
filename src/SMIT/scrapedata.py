"""
Tools for scraping data from website
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
    """Methods for interacting with webdriver module.

        Attributes
        ----------
        app : class instance
            Holds user information

        Methods
        -------
        wait_and_click(elementXpath):
            Wait for web element and click.
        _ff_options(dl_folder, headless):
            Set options for firefox webdriver.
        start_date_updater(dates):
            Update runtime dates in dates dict.
        _sng_input_dates(input_date):
            Fill dates in date-input web element.
        sng_login(dl_folder, headless):
            Login to stromnetz graz webportal and setup data page.
        _sng_fill_dates_element(start, end):
            Activate day sum web-element and fill start/end dates.
        _sng_start_download():
            Start download from webpage.
        _sng_switch_day_night_meassurements(day_night):
            Switch between day/night meter.
        get_daysum_files(headless):
            Download data summarized by day.
        _decode_password():
            Decode password from user instance and return plain text string.
    """
    def __init__(self, app: 'Application') -> None:
        """Initialize class with all attributes from user config files.

        Parameters
        ----------
        app : class instance
            Holds the configuration data for program run.
        """
        self.user = app
        self.driver = None
        self.logger = app.logger
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)

    def wait_and_click(self, elementXpath: str) -> None:
        """Wait for web element and click.

        Timeout 10s.

        Parameters
        ----------
        elementXpath : XPATH
            `xpath` of the element to click on
        """
        switchName = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, elementXpath))
        )
        switchName.click()

    def _ff_options(self, dl_folder: str,
                    headless: bool) -> webdriver.FirefoxOptions:
        """Set options for firefox webdriver.

        Parameters
        ----------
        dl_folder : folder path
            Target donwload directory for Firefox webdriver.
        headless : bool, optional
            Activate Firefox headless mode.

        Returns
        -------
        webdriver profile
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

        self.user.persistence.save_dates_log(dates)

    def _decode_password(self) -> str:
        """Get encoded password return decoded password.

        The password will be send in plain text.
        At the moment I see no other option.

        Parameters
        ----------
        pwd_string : str
            Encoded password.

        Returns
        -------
        str
            Decoded plain text password string.
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
        """Login to Stromnetz Graz webportal and setup data page.

        Parameters
        ----------
        dl_folder : folder path
            Target donwload directory for Firefox webdriver.
        headless : bool, optional
            activate Firefox headless mode, by default False
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
        """Pass start/end date to Stromnetz Graz website.

        Fill in start/end date and click trough web form.

        Parameters
        ----------
        input_date : string
            Date with format dd-mm-yyyy
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
        """Activate day sum web-element and fill start/end dates.

        Parameters
        ----------
        start : string
            Date with format dd-mm-yyyy
        end : string
            Date with format dd-mm-yyyy
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
        """Click download button web-element.
        """
        self.wait_and_click('/html/body/div/app-root/main/div/app-overview/reports-nav/app-header-nav/nav/div/div/div/div/div[2]/div/div[3]/div/div[2]/span')

    def _sng_switch_day_night_meassurements(self, day_night: str) -> None:
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

    def get_daysum_files(self, headless: bool = False) -> None:
        """Initiate '.csv' files download for day sum files.

        Parameters
        ----------
        headless : bool, optional
            Run Firefox in headless mode defaults to `False`.
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
