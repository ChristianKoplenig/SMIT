from datetime import date, timedelta
import pickle
import os.path

start_date = '01-01-2023'
end_date = '02-01-2023'

def date_persist():
    '''
    get yesterdays date and persist it for future start date in date_updater function
    '''
    path = './scrape_log.pkl'
    if not os.path.isfile(path):
        with open('scrape_log.pkl', 'wb') as pk:
            scrape_log = []
            scrape_log.append((date.today() - timedelta(days=1)).strftime('%d-%m-%Y'))
            pickle.dump(scrape_log, pk)
        pk.close()
    else:
        with open('scrape_log.pkl', 'rb') as pk:    # append today to logfile
            scrape_log = pickle.load(pk)
            if not (scrape_log[-1] == (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')): # check if yesterdays date already in log
                scrape_log.append((date.today() - timedelta(days=1)).strftime('%d-%m-%Y'))
                print('appended yesterdays date to scrape_log: ' + str(scrape_log))
            else:
                print('yesterdays date already persisted')
        pk.close()
        with open('scrape_log.pkl', 'wb') as pk:    # save logfile
            pickle.dump(scrape_log, pk)
        pk.close()
    return scrape_log

def date_updater():
    '''
    update start/end date for automated date setup
    '''
    global start_date
    global end_date
    start_date= date_persist()[-1]
    end_date = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
    return start_date, end_date

print('start before: ' + start_date)
print('end before: ' + end_date)
print('type start before: ' + str(type(start_date)))
date_updater()
print('-'*10)
print('start after: ' + start_date)
print('end after: ' + end_date)
print('type start after: ' + str(type(end_date)))