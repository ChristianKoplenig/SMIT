![Tests](https://github.com/tmpck/strom/actions/workflows/tests.yml/badge.svg)

# <p align="center">**SMI Tool** </p>
**<p align='center'> Smart Meter Interface Tool </p>**   
<p align='center'> Conveniently show and update your power usage </p>

## Intention
My main motivation for this application is to strengthen my coding skills and learn how to integrate libraries I have not used so far. Second it is also a playground for different methods to design a application. Third it is meant as a showcase for my coding skills and what I'm playing around with.

## About
The repository is a static fork of my `in progress` repo. I don't plan to update it regularly however if I implement some cool new features in my private repo I may push them to the public fork. I'm **very happy** about user input but won't promise anything about implementing it. Additionally web scraping is alway messy and if the "Stromnetz Graz" company changes anything at their website I wont promise to fix the scraper. However if I have the personal need for fixing it then I can promise that I will push the fix to the public repository.

## Disclaimer
The password is send in plain text to the login field. This is **not good practice**
but webscraping is per definition somehow messy. If you **save the password** 
it is stored in `program_root/user_data.toml` encrypted with the public key
generated by the program and stored in `program_root/keys` folder. The keys folder
is included in `.gitignore` make shure to **not expose the private key**.
Again this is not good practice but this project is about learning different
tools and coding.

## Requirements
The virtual environment was created with **Python 3.11** as base.
See `requirements.txt` for all needed dependencies. 

## Participating Guidlines
- Input is appreciated
- We want to keep the project language english, however we understand german and comments, pr's and so on in german are welcome too. 

## Folderstructure
- `root` --> Folder for Jupyther Notebook files and `user_data.py` file
- `csv_raw` --> Download folder for webdriver
- `csv_workdir` --> Python working directory
- `log` --> Folder to store log-files
- `modules` --> Folder for `module.py` files --> **Outdated**
- `opt` --> Folder for **not** programm related stuff (shared files, testfiles...) 
- `src` --> not so sure what to put in there to not interfere with testing routine
- `config` --> config files, user_data; user_settings; rsa-keys

## Branches
### main
- Scrape data - tested on win/linux.
- Perist date values for automated scraping workflow.
- Move files to input directory for python analysis.
- Modules as classes, first iteration
- Create dataframes for further analysis. 
### develop
- Modules as classes, pep8 implemented
- Temporarily store encrypted password in user class.
- Readme -> added disclaimer and about
### feature/pwd_dialog
- Get password
- Temporarily store encrypted password in user class.
- Option to store encrypted password permanently in user_data.py



## Licence
This project is under **insert_licence**. 

## Aknowledgements
I would like to thank [mike_landl](https://github.com/mike-landl) for all the 
code contributions, input on best practice, things to think about and generall
guiding how to write clean code! 

---

# <p align='center'> OLD Version </p>

# Stromnetz Graz - Analyse Data from Smartmeter
Automatically scrape and plot the data from 'Stromnetz Graz' web portal.
## Setup
Fill out user credentials in `user_data.py` located in `root` folder.  
In `root` folder create:  
- csv_raw folder
- csv_workdir folder

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
- `__pathlib_move(src, dest, appendix)`
	- Move and rename files
	- **Input:** source filepath, destination filepath, text to append
- `move_files_to_workdir.py(meter_number)`
	- Select files in webdriver download folder
	- Filter files with creation date today
	- Distinguish between files with different meter numbers
	- Call `__pathlib_move()`
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
- `load_dates_log()`
	- Load `dates` dict from storage to namespace
	- **Return:** `dates`
- `save_dates_log(dates)`
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
- `__sng_input_dates(input_date)`
	- Input start/end dates in web element
	- **Input:** date for `csv` file
- `sng_login(dl_folder, headless)`
	- Load firefox instance
	- Open website
	- Login
	- Go to data page
	- Set units
	- **Input:** path to download folder, headless mode for firefox
- `__sng_fill_dates_element(start, end)`
	- Activate web element for `daysum` download
	- use `__sng_input_dates()` to populate date fields
	- **Input:** start/end dates for file download
- `__sng_start_download()`
	- Push download button
- `__sng_switch_day_night_meassurements(day_night)`
	- Make dropdown menu for power meter input active
	- Choose second entry if input is `night_meter`, else choose first entry
	- **Input:** either day or night meter number
- `get_daysum_files(headless)`
	- Initialize dates logfile
	- Update end date for scraping
	- Check if files for today are already downloaded
	- Call functions to download files
	- **Input:** headless switch