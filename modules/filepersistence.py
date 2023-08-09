"""
Tools to persist data
"""
import pickle
from pathlib import Path
from datetime import date, timedelta

class persistence():
    """Class for dealing with all the data that needs to be peristed 
    
        Methods
        -------
        initialize_dates_log
        create_dates_var
        save_dates_loggingFile
    """
    def __init__(self, UserClass: 'modules.user.user') -> None:
        """Initialize Class with all attributes from `UserClass`

        Parameters
        ----------
        UserClass : class type
            User data initiated via `user()` function from user module            
        """
        # vars() creates dict 
        # items() iterate over key/value pairs       
        for key, value in vars(UserClass).items():
            setattr(self, key, value)
            
    def initialize_dates_log(self) -> None:
        """Create log file for managing scraping dates.

        If no persisted date exists, create dict for dates and use start date from user settings.
        """
        if not Path.is_file(self.persist_dates):
            with open(self.persist_dates, 'wb') as pk:
                dates = dict()
                # Initial run setup
                # Date format: dd-mm-yyyy
                dates['start'] = self.csv_startDate 
                dates['end'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
                dates['last_scrape'] = 'never'
                pickle.dump(dates, pk)
            pk.close()

    def create_dates_var(self) -> dict:
        """Load dates log dict.
        
        Loads the date logging variable from disc. 

        Returns
        -------
        dict
            [start], [end] and [last scrape] dates
        """
        with open(self.persist_dates, 'rb') as pk:
            dates = pickle.load(pk)
        return dates

    def save_dates_loggingFile(self, dates: dict):
        """Persist dates in log dict.
        
        Writes the dates logging variable to the disc.

        Parameters
        ----------
        dates : dict
            [start], [end], [last scrape]
        """
        with open(self.persist_dates, 'wb') as dpk:
            pickle.dump(dates, dpk)
        dpk.close()
        
    def __repr__(self) -> str:
        return str(vars(self))
        
    def __str__(self) -> str:
        return self.username