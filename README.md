# <p align="center">**SMIT** </p>
**<p align='center'> Smart Meter Interface Tool </p>**   
<p align='center'> Download and show your power usage </p>


## Intention

My main motivations for this application are to 
- simplify monitoring my power consumption
- strengthen my coding skills and learn how to integrate libraries I have not used so far 
- a playground for different methods to design applications
- showcase for my coding skills and what I'm playing around with

My goal is to make data which already exists easy acessible. I hope that this data
make users aware of their power consumption patterns. Maybe some of them will then
use this knowledge to **save energy**.

## TOC

 * [Intention](#intention)
 * [About](#about)
 * [Usage](#usage)
 * [Roadmap](#roadmap)
 * [Testing](#testing)
 * [Issues](#issues)
 * [Documentation](#documentation)
 * [Disclaimer](#disclaimer)
 * [Requirements](#requirements)
 * [Participation Guidlines](#participating-guidlines)
 * [Folderstructure](#folderstructure)
 * [Implementations](#implementations)
 * [License](#license)
 * [Acknowledgements](#acknowledgements)

## About
The repository is a static fork of my `in progress` repo. I don't plan to update it regularly however if I implement some cool new features in my private repo I may push them to the public fork. 

I'm **very happy** about user input but won't promise anything about implementing it. 

Additionally web scraping is always messy and if the "Stromnetz Graz" company changes anything at their website I wont promise to fix the scraper. However if I have the personal need for fixing it then I can promise that I will push the fix to the public repository.

## Usage
- In project root folder open `Main.ipynb`.
### Dummy usage
This mode is used for demonstration purposes and testing via pytest.
No "Stromnetz Graz" account is needed.
The Gui and scraping modules are not used.
The dummy data from `./opt/dummy_user` folder is used to setup a application mockup.
This will create a temporary `.dummy` folder in the project directory.
At the beginning of each dummy run the temporary folder will be deleted and newly created.

### Live data usage

<p align="center">
  <img src="./docs/readme/credentials_gui.png" width=35% /> 
  <br>
<br>
<ins><b><i> User Credentials GUI </i></b></ins>
</p>

Running with live data will first open a simple dialog to enter the "Stromnetz Graz" account data.
Username and password are provided by the elictricity provider. Your meter numbers are either found in
the "Netzzugangsvertrag" under "Technische Details - Zählpunkt/Gerät"  from the electricity provider or you can get them online following these steps:

<details>
	<summary>Get Meter Numbers</summary>

1. Open https://webportal.stromnetz-graz.at/login
2. Login
3. Choose "Auswertung"
4. In the "Zählpunktnummer" pull down menu you can see your meter numbers.

<p align="center">
  <img src="./docs/readme/select_meter.png" width=70% /> 
  <br>
<br>
<ins><b><i> "Stromnetz Graz" Data Page </i></b></ins>
</p>
</details>

You can use the 'Save user credentials' option to store your credentials in the `user_data.toml` file.
This file is located in the `./config` folder. See the disclaimer for information on password
storage and handling.
The buttons do exactly what their respective name implies. Implementation details are explained
in the [documentation](#documentation) section.

### Example output
At the moment the output is a really simple overview of your power usage. In future releases the 
output will feature more detailed plots to get usefull insights regarding the own power consumption.

<p align="center">
  <img src="./docs/readme/jnb_output.png" width=100% /> 
  <br>
<br>
<ins><b><i> Power Usage Sample Plot </i></b></ins>
</p>
</details>

## Roadmap
This roadmap is in no particular order. The priorization depends on which topic catches me the most at a given time.

- API access -> Depends on availability of public API
- Switch from Jupyter Notebook to modern GUI
- Use Sphinx for documentation
- Implement database
- Create executable package
- More detailed data plots
- Enhance logging / Debug option
- Implement more electricity providers

## Testing

**All tests are run in dummy configuration**  

From the command line in the root directory run `tox` command.

### Setup
Tests are located in the `./tests` folder.  
As test framework the pytest library is used.  
For managing and running the tests `tox` is used.  
For each module a test file with the
module name and the prefix 'test_' is used.  

### Tox Configuration
Environment: Python 3.11  
Test Setup: `tox.ini`  
Markers: `pyproject.toml`  
   

## Issues
- No Decline button in GUI
- Main.ipynb -> Log gets printed multible times
- Rsa Keys on initial run not working
- SNG Data update not implemented

## Documentation
The documentation for this project is done via docstrings. As format for the 
docstrings the [Google Style Guide](https://google.github.io/styleguide/pyguide.html) is used. 
I think it is good practice to invest time in writing detailed docstrings and thus the documentation is done on the fly.

At the moment I use the pdoc3 library to generate html output from the docstrings.
In future I want to switch to sphinx in combination with the readthedocs theme. Ideally
this leads to a more compact documentation and a simpler README file. 

The documentation for the modules and methods is found here: [Application](https://filedn.eu/liu4e7QL6NoXLInqRT2UAQu/SMIT/index.html)  
All tests are documented here: [Tests](https://filedn.eu/liu4e7QL6NoXLInqRT2UAQu/tests/index.html)  

## Disclaimer
The password is send in plain text to the login field. This is **not good practice**
but webscraping is per definition somehow messy. If you **save the password** 
it is stored in `program_root/config/user_data.toml` encrypted with the public key
generated by the program and stored in `program_root/config` folder. The keys are included 
in `.gitignore` make shure to **not expose the private key**.
Again this is not good practice but this project is about learning different
tools and coding. 

## Requirements
The virtual environment was created with **Python 3.11** as base.  
See [requirements.txt](./requirements.txt) for all needed dependencies. 

## Participating Guidlines
- Input is appreciated
- We want to keep the project language english, however we understand german and comments, pr's and so on in german are welcome too. 

## Folderstructure
- `root` 
	- --> Project home
- `csv_raw` 
	- --> Folder for webdriver downloads   
	- --> Raw `.csv` files are stored in subdirectories
- `csv_workdir` 
	- --> Python working directory
	- --> Pandas input `.csv` files are stored in subdirectories
- `log` 
	- --> Logfiles
- `opt` 
	- --> **Dummy Configs** are stored in a subdirectory
	- --> Folder for develop files, testfiles... 
- `src` 
	- --> Source code folder
	- --> `SMIT` --> **Modules directory**
- `config` 
	- --> user config files, rsa-keys
- `docs`
	- --> **Pdoc3** generated modules documentation
- `tests`
	- --> **Pytest** source folder
- `.dummy`
	- --> Get's created when application class is instantiated with **dummy option**
	- --> on each instantiation folder gets **deleted and newly created**
- `.tox`
	- --> Data for running tests

## Implementations
### Libraries

- **Pickle** - Perist date values for automated scraping workflow.
- **Pathlib** - Folder structure setup
- **Pathlib** - Move files to input directory for python analysis.
- **Tomlkit** - Manage configs in `.toml` files
- **Logger** - Log Application modules
- **Rsa** - Encrypted password storage
- **Selenium Webdriver** - Scrape data
- **Tkinter** - Gui for user credentials
- **Pandas** - Create dataframes for further analysis. 
- **Pytest** - Test Application modules
- **Pdoc** - Generate documentation from docstrings

### Application modules

**application** - Provide core functionality
**filehandling** - File operation related methods
**filepersistence** - Preserve data via serialization
**rsahandling** - Public key cryptography
**scrapedata** - Selenium webdriver implementation
**userinput** - Simple User Credentials Gui 

## Acknowledgements
I would like to thank [mike_landl](https://github.com/mike-landl) and [martinhecher](https://github.com/martinhecher) for all the code contributions, input on best practice, things to think about and generall 
guiding how to write clean code! 

## License
This project is developed under the [MIT License](LICENSE). 