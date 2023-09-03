"""
    Tools for manipulating files on os basis
        Classes:
        --------
        OsInterface:
            Os file operations
            Generate Python data frame
        TomlTools:
            Read/Write `.toml` files
            Append password
"""
import datetime as dt
import pathlib as pl
import pandas as pd
import tomlkit
# Type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from SMIT.application import Application

class OsInterface():
    """Methods for interacting with files on os filesystem.

        Attributes
        ----------
        app : class instance
            Holds user information

        Methods
        -------
        _pathlib_move(src, dest, appendix):
            Move and rename files.
        move_files_to_workdir(meter_number):
            Filter files and run _pathlib_move().
        create_dataframe(workdir, metertype):
            Create initial dataframe.
        scrapeandmove():
            Initiate download process and move files.
    """
    def __init__(self, app: 'Application') -> None:
        """Initialize Class with all attributes from `UserClass`

        Parameters
        ----------
        app : class instance
            Holds the configuration data for program run.
        """
        self.user = app
        self.logger = app.logger
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)

    def _pathlib_move(self, src: pl.Path,dest: pl.Path,appendix: str) -> None:
        """Use pathlib to move and rename file.

        Move the file from `src` to `dest` and rename it to todays date (yyyy-mm-dd) folowed by '_appendix.csv'.
        File will get a '.csv' extension.

        Parameters
        ----------
        src : pathlib path
            Path to source file
        dest : pathlib path
            Path to destination file
        appendix : string
            String to append to filename
        """
        path = pl.Path(src)
        new_filename = dest / str(str(dt.date.today().strftime('%Y%m%d') + '_' + str(appendix)) + '.csv')
        path.rename(new_filename)

    def move_files_to_workdir(self, meter_number: str) -> None:
        """Move files from download dir to work dir.

        Iterate over all '.csv' files in webdriver download folder.
        Select files with creation date of today.
        Select files with `meter_number` in filename.
        For selected files run :func: `_pathlib_move`.

        Parameters
        ----------
        meter_number : string
            Day/Night meter device number
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

                #filter for input files
                if meter_number in str(filename):
                    self._pathlib_move(filename, workdir, meter_number)
                    self.logger.debug(f'Moved file for meter: {meter_number} to workdir')

    def create_dataframe(self, workdir: pl.Path, metertype: str) -> pd.DataFrame:
        """Create basic dataframe for further analysis.

        Concat all files in `workdir` with same `metertype`.
        Delete unused columns.
        Convert date format.
        Set column dtype formats.
        Sort values by date.
        Drop duplicates.

        Parameters
        ----------
        workdir : pathlib path
            Path to directory with files to import.
        metertype : string
            Day/Night meter device number.

        Returns
        -------
        dataframe
            Pandas dataframe with values per meter.
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
                    usecols=lambda x: x in ['date', 'zaehlerstand', 'verbrauch'],
                ) for file in filelist
            )
        )

        df_return['zaehlerstand'] = df_return['zaehlerstand'].astype(float)
        df_return['verbrauch'] = df_return['verbrauch'].astype(float)
        df_return.sort_values(by='date', inplace=True)
        df_return.reset_index(drop=True, inplace=True)
        df_return.drop_duplicates(subset='date', keep='first', inplace=True)
        self.logger.debug(f'Created pandas dataframe for meter: {metertype}')
        return df_return

    def sng_scrape_and_move(self) -> None:
        """Scrape data and move '.csv' files to workdir.

        Call :func: `get_daysum_files`
        For each meter call :func: `move_files_to_workdir`
        """
        self.user.persistence.initialize_dates_log()
        dates = self.user.persistence.load_dates_log()

        # scrape just once a day
        if not dates['start'] == dt.date.today().strftime('%d-%m-%Y'):

            self.user.scrape.get_daysum_files(self.user.Options['headless_mode'])
            self.move_files_to_workdir(self.user.Meter['day_meter'])
            self.move_files_to_workdir(self.user.Meter['night_meter'])
        else:
            self.logger.info('Most recent data already downloaded')

    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"


class TomlTools():
    """Class for handling toml files
        Attributes
        ----------
        user : class instance
            Holds user information

        Methods
        -------
        load_toml_file(filename):
            Return toml object from filesystem.
        save_toml_file(filename, toml_object):
            Write toml object to filesystem.
        _append_password(toml_object, pwd)
            Append password to toml object
        add_password_to_toml(toml_filename, password)
    """
    def __init__(self, app: 'Application') -> None:
        """Initialize class with all attributes from user config files.

        Parameters
        ----------
        app : class instance
            Holds the configuration data for program run.
        """
        self.user = app
        self.user_data = pl.Path(self.user.Path['user_data'])
        self.logger = app.logger
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)

    def load_toml_file(self, filename: pl.Path) -> tomlkit.TOMLDocument:
        """Read `.toml` file and return Python TOML object.

        Parameters
        ----------
        filename : pl.Path
            Path object to the `.toml` file.

        Returns
        -------
        object
            Python TOML object
        """
        with open(filename, mode='rt', encoding='utf-8') as file:
            data = tomlkit.load(file)
        return data

    def save_toml_file(self, filename: pl.Path, toml_object: tomlkit.TOMLDocument) -> None:
        """Takes python TOML object and writes `.toml` file to filesystem

        Parameters
        ----------
        filename : pl.Path
            Path to output file on filesystem
        toml_object : tomlkit
            Python TOML object
        """
        with open(filename, mode='wt', encoding='utf-8') as file:
            tomlkit.dump(toml_object, file)

    def _append_password(self, toml_object: tomlkit.TOMLDocument, pwd: str) -> None:
        """Append password entry to Login table in Python TOML object.

        Parameters
        ----------
        toml_object : tomlkit
            Python TOML object.
        pwd : str
            Password for web scraping login.
        """
        try:
            if 'password' in toml_object['Login']:
                raise KeyError('Password already saved')
            else:
                toml_object['Login'].add("password", pwd) # pylint: disable=no-member
                toml_object['Login']['password'].comment('Permission to store password given')
        except KeyError as e:
            self.logger.error(e)

    def add_password_to_toml(self, toml_filename: pl.Path, password: str) -> None:
        """Add password to `user_data.toml`.

        Parameters
        ----------
        toml_filename : pl.Path
            Path to `.toml` file
        password : str
            Password for web scraping login.
        """
        # Store password in user_data.toml
        user_data = self.load_toml_file(toml_filename)
        self._append_password(user_data, password)
        self.save_toml_file(toml_filename, user_data)
        self.logger.debug('Password added to user data')

    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"