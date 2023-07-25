from datetime import date, timedelta
import pickle
import os.path

dates = dict()
dates['start'] = '01-01-2023'
dates['end'] = '02-01-2023'

def date_persist():
    '''
    get yesterdays date and persist it for future start date in date_updater function
    '''
    path = './dates.pkl'
    if not os.path.isfile(path):
        with open('dates.pkl', 'wb') as pk:
            global dates
            dates['last_scrape'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
            pickle.dump(dates, pk)
        pk.close()
    else:
        with open('dates.pkl', 'rb') as pk:    # append today to logfile
            dates = pickle.load(pk)
            if not (dates['last_scrape'] == (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')): # check if yesterdays date already in log
                dates['last_scrape'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
                print('appended yesterdays date to dates: ' + str(dates['last_scrape']))
            else:
                print('yesterdays date already persisted')
        pk.close()
        with open('dates.pkl', 'wb') as pk:    # save logfile
            pickle.dump(dates, pk)
        pk.close()
    return dates

def date_updater():
    '''
    update start/end date for autofill
    '''
    global dates
    dates['start'] = date_persist()['last_scrape']
    dates['end'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
    return dates

print('start before: ' + dates['start'])
print('end before: ' + dates['end'])
print('type start before: ' + str(type(dates['start'])))
date_updater()
print('-'*10)
print('start after: ' + dates['start'])
print('end after: ' + dates['end'])
print('type start after: ' + str(type(dates['end'])))
print(dates)