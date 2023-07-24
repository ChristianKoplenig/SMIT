from datetime import date, timedelta
import pickle
import os.path

start_date = '01-01-2023'
end_date = '02-01-2023'

def date_pickle():
    '''
    get todays date and pickle it for future start date in date_updater function
    '''
    path = './scrape_log.pkl'
    if not os.path.isfile(path):
        with open('scrape_log.pkl', 'wb') as pk:
            scrape_log = []
            scrape_log.append((date.today() - timedelta(days=1)).strftime('%d-%m-%Y'))
            pickle.dump(scrape_log, pk)
        pk.close()
    else:
        with open('scrape_log.pkl', 'rb') as pk:
            scrape_log = pickle.load(pk)
            scrape_log.append((date.today() - timedelta(days=1)).strftime('%d-%m-%Y'))
            print('opend log: ' + str(scrape_log))
        pk.close()
        with open('scrape_log.pkl', 'wb') as pk:
            pickle.dump(scrape_log, pk)
        pk.close()
    return scrape_log

def date_updater():
    '''
    update start/end date for automated date setup
    '''
    global start_date
    global end_date
    start_date= date_pickle()[-1]
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