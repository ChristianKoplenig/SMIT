"""Serialize objects

---
`Persistence`
------------

- Initialize variable for scrape dates logging.
- Load serialized dates log variable.
- Store dates log variable as pickle object.

Typical usage:

    app = Application()
    app.persistence.method()
"""
import pickle
from pathlib import Path
from datetime import date, timedelta
# Type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from SMIT.application import Application


class Persistence():
    """Persist dates for scraping routine.
    
    ---
    
    Initialize a variable to store and persist date of last
    scraping run. Assure that start and end dates of last
    scraping run are stored between programm runs. On first run
    set the start date to the date stored in `user_settings.toml`. 

    Attributes:
        app (class): Accepts `SMIT.application.Application` type attribute.
    """
    def __init__(self, app: 'Application') -> None:

        self.user = app
        self.logger = app.logger
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)

    def initialize_dates_log(self) -> None:
        """Create log file for managing scraping dates.

        If no persisted date exists, 
        create dict for dates and use start date from user settings.
        """
        # Initial run
        if not Path(self.user.Path['persist_dates']).exists():
            with open(self.user.Path['persist_dates'], 'wb') as pk:
                dates = dict()
                # Date format: dd-mm-yyyy
                dates['start'] = self.user.Init['csv_startDate']
                dates['end'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
                dates['last_scrape'] = 'never'
                pickle.dump(dates, pk)
            pk.close()
        self.logger.debug('Dates log initialized')

    def load_dates_log(self) -> dict:
        """Deserialize `dates.pkl`.

        Load the date logging object from disc.  
        Make dates logging variable accessible for webscraper.

        Returns:
            dict: Keys: [`start`, `end`, `last scrape`].  
                - [`start`]: After each run set today's date for next run.  
                - [`end`]: End date (yesterday) for scraping.  
                - [`last_scrape`]: Store date between application runs. 
        """
        with open(self.user.Path['persist_dates'], 'rb') as pk:
            dates = pickle.load(pk)
        return dates

    def save_dates_log(self, dates: dict):
        """Serialize dates object.

        Store dates logging variable between application runs.

        Args:
            dates (dict): Variable for scrape date management.
        """
        with open(self.user.Path['persist_dates'], 'wb') as dpk:
            pickle.dump(dates, dpk)
        dpk.close()

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
