# Login credentials
login_url = 'https://webportal.stromnetz-graz.at/login'
username = 'ch.koplenig@posteo.net'
password = 'Gwhwk12.'

# Stromnetz Anlagedaten
day_meter = '199996'        # Zaehlpunktnummer Tagstrom; last six numbers
night_meter = '199997'      # Zaehlpunktnummer Nachtstrom; last six numbers


#################### not necessary to change ###############################

# Csv File Options
csv_startDate = '01-01-2023'            # Start date for initial run

# Firefox options
headless_mode = True                    # Run Firefox in headless mode, type: boolean

# Folder structure
## scraping
csv_dl_daysum = './csv_raw/daily'               # Download folder for Tageswerte csv files
csv_dl_15min = './csv_raw/15min'                # Download folder for 15min resolution csv files
persist_dates = './log/dates.pkl'               # Filename for dates persistence
webdriver_logFolder = './log/geckodriver.log'   # Log folder for webdriver
## working
csv_wd_daysum = './csv_workdir/daily'           # Location of files to process
csv_wd_15min = './csv_workdir/15min'