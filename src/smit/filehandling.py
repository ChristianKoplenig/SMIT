"""Classes for file operations.

---
`OsInterface`
-------------

- Move files to work directory.
- Rename files to preserve originally scraped data.
- Scrape and move workflow.
- Generate Python data frame.

Typical usage:

    app = Application()
    app.os_tools.method()
    
    
`TomlTools`
-----------

- Save and load `.toml` files
- Manipulate `.toml` files
    
    
Typical usage:

    app = Application()
    app.toml_tools.method()
"""
import datetime as dt
import pathlib as pl
import pandas as pd
import tomlkit
# Type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smit.application import Application


class OsInterface():
    """Manipulate data files.
    
    ---
    
    Download and prepare `.csv` files.  
    Read `.csv` files and provide pandas dataframe.  
    
    Attributes:
        app (class): Accepts `SMIT.application.Application` type attribute.
    """
    
    def __init__(self, app: 'Application') -> None:
        
        self.user = app
        self.logger = app.logger
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)

    def _pathlib_move(self, src: pl.Path, dest: pl.Path, appendix: str) -> None:
        """Use pathlib to move and rename file.

        Move the file from `src` to `dest` folder 
        and rename it to todays date (yyyy-mm-dd) with '_appendix.csv' added.

        Args:
            src (pathlib.Path): Path to source file.
            dest (pathlib.Path): Path to destination folder.
            appendix (string): String to append to filename.
        """
        path = pl.Path(src)
        new_filename = dest / str(str(dt.date.today().strftime('%Y%m%d') + '_' + str(appendix)) + '.csv')
        path.rename(new_filename)

        self.logger.debug(f'File: {src} moved to: {new_filename}')

    def _move_files_to_workdir(self, meter_number: str) -> None:
        """Move files from download dir to work dir.

        - Iterate over all `.csv` files in webdriver download folder.  
        - Select files with creation date of today.  
        - Select files with `meter_number` in filename.  
        - For selected files run `SMIT.filehandling.OsInterface._pathlib_move`.  

        Args:
            meter_number (string): Day/Night meter device number.
        """
        # set path variables
        path_to_raw = pl.Path(self.user.Folder['raw_daysum']).absolute()
        workdir = pl.Path(self.user.Folder['work_daysum']).absolute()

        # select files in raw folder
        for filename in path_to_raw.glob('*.csv'):
            filename_cdate = filename.stat().st_ctime
            cdate = dt.datetime.fromtimestamp(filename_cdate).strftime('%Y-%m-%d')

            # just process downloaded files from today
            if cdate == dt.date.today().strftime('%Y-%m-%d'):

                # filter for input files
                if meter_number in str(filename):
                    self._pathlib_move(filename, workdir, meter_number)
                    self.logger.debug(f'Moved file for meter: {meter_number} to workdir')

    def create_dataframe(self, workdir: pl.Path, metertype: str) -> pd.DataFrame:
        """Read `.csv` files and create pandas dataframe.

        - Concat all files in `workdir` with same `metertype`.
        - Delete unused columns.
        - Convert date format.
        - Set column dtype formats.
        - Sort values by date.
        - Drop duplicates.

        Args:
            workdir (pathlib.Path): Path to directory for file import.
            metertype (string): Day/Night meter device number.

        Returns:
            pandas.DataFrame: With columns [`date`, `zaehlerstand`, `verbrauch`] for each meter.
        """
        path = pl.Path(workdir)
        df_return = pd.DataFrame()

        filelist = [filename for filename in path.glob('*.csv') if str(metertype) in filename.name]

        df_return = pd.concat(
            (pd.read_csv(
                file,
                sep=';',
                decimal=',',
                header=0,
                parse_dates=['date'],
                converters={'date': lambda t: dt.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%f%z').date()},
                names=['date', 'zaehlerstand', '1', '2', 'verbrauch', '3', '4'],
                usecols=lambda x: x in ['date', 'zaehlerstand', 'verbrauch'])
                for file in filelist)
        )

        df_return['zaehlerstand'] = df_return['zaehlerstand'].astype(float)
        df_return['verbrauch'] = df_return['verbrauch'].astype(float)
        df_return.sort_values(by='date', inplace=True)
        df_return.reset_index(drop=True, inplace=True)
        df_return.drop_duplicates(subset='date', keep='last', inplace=True)
        df_return['rol_med_30'] = df_return['verbrauch'].rolling(30).median().round(decimals=2)
        df_return['rol_med_7'] = df_return['verbrauch'].rolling(7).median().round(decimals=2)
        
        self.logger.debug(f'Created pandas dataframe for meter: {metertype}')
        
        return df_return

    def sng_scrape_and_move(self) -> None:
        """Download and move `.csv` files.

        - Determine if method was already called with today's date.
        - If not call `SMIT.scrapedata.Webscraper.get_daysum_files`.
        - Use `SMIT.filehandling.OsInterface._move_files_to_workdir` 
        to move files to work directory.
        
        Info:
            With dummy option active only 
            `SMIT.filehandling.OsInterface._move_files_to_workdir`
            will be called.
        """
        if self.user.dummy is False:
            self.user.persistence.initialize_dates_log()
            dates = self.user.persistence.load_dates_log()

            # Scrape just once a day
            if dates['last_scrape'] == dt.date.today().strftime('%d-%m-%Y'):
                self.logger.info('Most recent data already downloaded')
            else:
                self.user.scrape.get_daysum_files(self.user.Options['headless_mode'])
                self._move_files_to_workdir(self.user.Meter['day_meter'])
                self._move_files_to_workdir(self.user.Meter['night_meter'])
        else:
            # Move files for dummy user
            self._move_files_to_workdir(self.user.Meter['day_meter'])
            self._move_files_to_workdir(self.user.Meter['night_meter'])
            self.logger.debug('Files for dummy user moved to workdir')

    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"

class TomlTools():
    """Manipulate config files.

    ---
    
    Load and save `.toml` config files.  
    Add and delete entries from config files.

    Attributes:
        app (class): Accepts `SMIT.application.Application` type attribute.    
    """
    def __init__(self, app: 'Application') -> None:

        self.user = app
        self.user_data = pl.Path(self.user.Path['user_data'])
        self.logger = app.logger
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)

    def load_toml_file(self, filename: pl.Path) -> tomlkit.TOMLDocument:
        """Read `.toml` file and return Python TOML object.

        Args:
            filename (patlib.Path): Path object for the configuration file.

        Returns:
            tomlkit.TOMLDocument: Editable configuration object.
        """
        with open(filename, mode='rt', encoding='utf-8') as file:
            data = tomlkit.load(file)

        self.logger.debug(f'Toml file {filename} read')
        return data

    def save_toml_file(self, filename: pl.Path, toml_object: tomlkit.TOMLDocument) -> None:
        """Accepts TOML object and writes file to filesystem.

        Args:
            filename (pathlib.Path): Destination for config file.
            toml_object (tomlkit.TOMLDocument): Configuration object to save.
        """
        with open(filename, mode='wt', encoding='utf-8') as file:
            tomlkit.dump(toml_object, file)

        self.logger.debug(f'Toml file: {filename} written')

    def add_entry_to_config(self, toml_path: pl.Path,
                            section: str,
                            config_attribute: str,
                            entry: str) -> None:
        """Load config file, select table and add entry.

        Use for input from Tkinter Gui.  
        If an entry exists it will be overwritten.  

        Args:
            toml_path (pathlib.Path): Path object for the configuration file.
            section (string): Table name in config file.
            config_attribute (string): Attribute in config file to update.
            entry (string): String to store in config file.
        """
        config = self.load_toml_file(toml_path)
        config[section][config_attribute] = entry
        config[section][config_attribute].comment('Data collected via Gui')
        self.save_toml_file(toml_path, config)
        self.logger.debug(f'{config_attribute} added to {toml_path}')

    def delete_entry_from_config(self,
                                 toml_path: pl.Path,
                                 section: str,
                                 config_attribute: str) -> None:
        """Load config file, select table and delete attribute.

        Use for input from Tkinter Gui.  
        Table entry and config attribute will be deleted.

        Args:
            toml_path (pathlib.Path): Path object for the configuration file.
            section (string): Table name in config file.
            config_attribute (string): Attribute in config file to update.
        """
        config = self.load_toml_file(toml_path)
        del config[section][config_attribute]
        self.save_toml_file(toml_path, config)
        self.logger.debug(f'{config_attribute} deleted from {toml_path}')

    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"


# Pdoc config get underscore methods
__pdoc__ = {name: True
            for name, classes in globals().items()
            if name.startswith('_') and isinstance(classes, type)}


__pdoc__.update({f'{name}.{member}': True
                 for name, classes in globals().items()
                 if isinstance(classes, type)
                 for member in classes.__dict__.keys()
                 if member not in {'__module__', '__dict__',
                                   '__weakref__', '__doc__'}})

__pdoc__.update({f'{name}.{member}': False
                 for name, classes in globals().items()
                 if isinstance(classes, type)
                 for member in classes.__dict__.keys()
                 if member.__contains__('__') and member not in {'__module__', '__dict__',
                                                                 '__weakref__', '__doc__'}})
