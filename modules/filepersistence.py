"""
Tools to persist data
"""
import os
import pickle
from datetime import date, timedelta
# Custom imports
from modules.user import user

User = user()

def initialize_dates_log():
    """Create log file for managing scraping dates.

    If no persisted date exists, create dict for dates and use start date from User.
    """
    if not os.path.isfile(User.persist_dates):
        with open(User.persist_dates, 'wb') as pk:
            dates = dict()
            dates['start'] = User.csv_startDate                                        # set start date for initial run, format: dd-mm-yyyy
            dates['end'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')          # set end date yesterday for initial run, format: dd-mm-yyyy
            dates['last_scrape'] = 'never'                                                  # flag for first run
            pickle.dump(dates, pk)
        pk.close()

def create_dates_var():
    """Load dates log dict.

    Returns
    -------
    dict
        start, end and last scrape dates
    """

    with open(User.persist_dates, 'rb') as pk:
        dates = pickle.load(pk)
    return dates

def save_dates_loggingFile(dates):
    """Persist dates in log dict.

    Parameters
    ----------
    dates : dict
        start, end and last scrape dates
    """
    with open(User.persist_dates, 'wb') as dpk:                                                                        # save logfile
        pickle.dump(dates, dpk)
    dpk.close()