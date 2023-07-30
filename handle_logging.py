import os
import pickle
from datetime import date, timedelta
import user_data

def initialize_dates_log():
    ''' 
    create log file for managing scrape dates
    If no persisted date exists, create dict for dates and use start date from user_data
    '''
    if not os.path.isfile(user_data.persist_dates):
        with open(user_data.persist_dates, 'wb') as pk:
            dates = dict()
            dates['start'] = user_data.csv_startDate                                        # set start date for initial run, format: dd-mm-yyyy
            dates['end'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')          # set end date yesterday for initial run, format: dd-mm-yyyy
            dates['last_scrape'] = 'never'                                                  # flag for first run
            pickle.dump(dates, pk)
        pk.close()

def create_dates_var():
    '''
    make dates log acessible
    '''   
    with open(user_data.persist_dates, 'rb') as pk:
        dates = pickle.load(pk)  
    return dates

def save_dates_loggingFile(dates):
    '''
    export dates logging file 
    '''
    with open(user_data.persist_dates, 'wb') as dpk:                                                                        # save logfile
        pickle.dump(dates, dpk)
    dpk.close()