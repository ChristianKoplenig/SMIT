# Stromnetz Graz - Analyse Data from Smartmeter
Automatically scrape and plot the data from 'Stromnetz Graz' web portal.
## Setup
Fill out user credentials in `user_data.py` located in `root` folder

## Test System
### OS
- Ubuntu 23.04 Standart Distro
- VSCode - direct install, no snap

### Tools
- Python 3.9.15
- Seaborn 0.12.1
- Matplotlib 3.5.3
- Pathlib 1.0.1
- Pandas 1.4.4
- Pickleshare 0.7.5
- Selenium 4.10.0
- Webdriver 115.0.2

## Folderstructure
- `root` --> Folder for Jupyther Notebook files and `user_data.py` file
- `csv_raw` --> Download folder for webdriver
- `csv_workdir` --> Python working directory
- `log` --> Folder to store log-files
- `modules` --> Folder for `module.py` files

## Modules
### `dynamicclass.py`
**Dynamically creates a `User` class from `user_data.py` files**  
`User` class makes all the user editable variables accesible 
- `create_user()`
	- Function to create user class
	- **Input:** path to user data file, class name

### `filehandling.py`
**Functions to deal with operating system folders**
- `pathlib_move(src, dest, appendix)`
	- Move and rename files
	- **Input:** source filepath, destination filepath, text to append
- `move_files.py(meter_number)`
	- Select files in webdriver download folder
	- Filter files with creation date today
	- Distinguish between files with different meter numbers
	- Call `pathlib_move()`
	- **Input:** number for power meter
- `scrapeandmove()`
	- Start downloading `csv` files from web portal
	- Copy files to python work directories
- `create_dataframe(workdir, metertype)`
	- Select all files in directory
	- Distinguish between day/night meter type
	- Combine all `csv` files to one dataframe
	- Convert date and time
	- Delete unused columns
	- Sort by date
	- Drop duplicates
	- **Return:** dataframe
	- **Input:** `csv` files directory, day/night meter type

### `filepersistence.py`
**Functions used to permanently store information on os filesystem (pickling)**
- `initialize_dates_log()
	- Create `dates` dict and fill for first run
	- Save `dates` dict to log folder
- `create_dates_var()`
	- Load `dates` dict from storage to namespace
	- **Return:** `dates`
- `save_dates_loggingFile(dates)`
	- Save `dates` dict to log folder
	- **Input:** File to save

### `scrapedata.py`
**Functions for interacting with the web portal**
- `wait_and_click(xpath)`
	- Wait for web element availability and click on it
	- **Input:** xPath of web element
- `ff_options(dl_folder, headless)`
	- Define options for firefox webdriver instance
	- **Input:** path to download folder, headless mode switch
- `start_date_updater(dates)`
	- Set and update start date for automated scraping
	- **Input:** `dates` dict
- `date_selector(input_date)`
	- Input start/end dates in web element
	- **Input:** date for `csv` file
- `stromnetz_setup(dl_folder, headless)`
	- Load firefox instance
	- Open website
	- Login
	- Go to data page
	- Set units
	- **Input:** path to download folder, headless mode for firefox
- `stromnetz_fillTageswerte(start, end)`
	- Activate web element for `daysum` download
	- use `date_selector()` to populate date fields
	- **Input:** start/end dates for file download
- `stromnetz_download()`
	- Push download button
- `day_night_selector(day_night)`
	- Make dropdown menu for power meter input active
	- Choose second entry if input is `night_meter`, else choose first entry
	- **Input:** either day or night meter number
- `get_daysum_files(headless)`
	- Initialize dates logfile
	- Update end date for scraping
	- Check if files for today are already downloaded
	- Call functions to download files
	- **Input:** headless switch