# Login credentials
login_url = 'https://webportal.stromnetz-graz.at/login'
username = 'ch.koplenig@posteo.net'
password = 'Gwhwk12.'

# Firefox options
headless_mode = False                    # Run Firefox in headless mode, type: boolean

# Folder structure
csv_dl_daysum = './csv_raw/daily'               # Download folder for Tageswerte csv files
csv_dl_15min = './csv_raw/15min'                               # Download folder for 15min resolution csv files
persist_dates = './log/dates.pkl'               # Filename for dates persistence
webdriver_logFolder = './log/geckodriver.log'   # Log folder for webdriver

# Csv File Options
csv_startDate = '01-01-2023'            # Start date for initial run