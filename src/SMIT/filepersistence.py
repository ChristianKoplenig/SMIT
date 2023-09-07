"""
Tools to persist data
"""
import pickle
from pathlib import Path
from datetime import date, timedelta
# Type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from SMIT.application import Application


class Persistence():
    """Methods to generate and access logging data.

        Attributes
        ----------
        user : class instance
            Holds user information

        Methods
        -------
        initialize_dates_log():
            Create `dates` log on first run
        load_dates_log():
            Make `dates` dict accessible
        save_dates_log():
            Saves `dates` log file
    """
    def __init__(self, app: 'Application') -> None:
        """Initialize class with all attributes from user config files.

        Parameters
        ----------
        app : class instance
            Holds the configuration data for program run.
        """
        self.user = app
        self.logger = app.logger
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)

    def initialize_dates_log(self) -> None:
        """Create log file for managing scraping dates.

        If no persisted date exists, create dict for dates and use start date from user settings.
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
        """Load dates log dict.

        Loads the date logging variable from disc.

        Returns
        -------
        dict
            [start], [end] and [last scrape] dates
        """
        with open(self.user.Path['persist_dates'], 'rb') as pk:
            dates = pickle.load(pk)
        return dates

    def save_dates_log(self, dates: dict):
        """Persist dates in log dict.

        Writes the dates logging variable to the disc.

        Parameters
        ----------
        dates : dict
            [start], [end], [last scrape]
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
