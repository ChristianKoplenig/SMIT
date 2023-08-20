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
# Custom modules
from modules.filepersistence import Persistence
from modules.scrapedata import Webscraper
from modules.user import user

class OsInterface():
    """Methods for interacting with files on os filesystem
        
        Attributes
        ----------
        user : class instance
            Holds user information      
        Methods
        -------
        pathlib_move(src, dest, appendix):
            Move and rename files.
        move_files(meter_number):
            Filter files and run pathlib_move().
        create_dataframe(workdir, metertype):
            Create initial dataframe.
        scrapeandmove():
            Initiate download process and move files.
    """
    def __init__(self, user: user) -> None:
        """Initialize Class with all attributes from `UserClass`

        Parameters
        ----------
        UserInstance : class type
            User data initiated via `user()` function from user module            
        """
        user : user
        
        self.user = user
            
    def pathlib_move(self, src: pl.Path,dest: pl.Path,appendix: str) -> None:
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

    def move_files(self, meter_number: str) -> None:
        """Copy files to work directory.

        Iterate over all '.csv' files in webdriver download folder.
        Select files with creation date of today.
        Select files with `meter_number` in filename.
        For selected files run :func: `pathlib_move`.

        Parameters
        ----------
        meter_number : string
            Day/Night meter device number
        """
        # set path variables
        path_to_raw = pl.Path(self.user.csv_dl_daysum).absolute()
        workdir = pl.Path(self.user.csv_wd_daysum).absolute()

        # select files in raw folder
        for filename in path_to_raw.glob('*.csv'):
            filename_cdate = filename.stat().st_ctime
            cdate = dt.datetime.fromtimestamp(filename_cdate).strftime('%Y-%m-%d')

            # just process downloaded files from today
            if cdate == dt.date.today().strftime('%Y-%m-%d'):

                #filter for input files
                if meter_number in str(filename):
                    self.pathlib_move(filename, workdir, meter_number)              

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
        return df_return

    def scrapandmove(self) -> None:
        """Scrape data and move '.csv' files to workdir.

        Call :func: `get_daysum_files`
        For each meter call :func: `move_files`
        """
        Persistence(self.user).initialize_dates_log()
        dates = Persistence(self.user).create_dates_var()
        
        # scrape just once a day
        if not dates['start'] == dt.date.today().strftime('%d-%m-%Y'):                 

            Webscraper(self.user).get_daysum_files(self.user.headless_mode)
            self.move_files(self.user.day_meter)
            self.move_files(self.user.night_meter)
        else:
            print('Most recent data already downloaded')
            
    def __repr__(self) -> str:
        return str(vars(self))
        
    def __str__(self) -> str:
        return self.user.username

    
class TomlTools():
    """Class for handling toml files
        Attributes
        ----------
        user : class instance
            Holds user information      
        
        Methods
        -------
        load_toml_file():
            Return toml object from filesystem.
        save_toml_file():
            Write toml object to filesystem. 
    
    """
    def __init__(self, user: user) -> None:
        self.user = user
        self.user_data = pl.Path(self.user.user_data_path)
        
    def load_toml_file(self, filename: pl.Path) -> tomlkit:
        """Read `filename` file and return TOML object.

        Parameters
        ----------
        filename : pl.Path
            Path object to the `.toml` file.

        Returns
        -------
        object
            TOML object
        """
        with open(filename, mode='rt', encoding='utf-8') as file:
            data = tomlkit.load(file)
            print('type: ' + str(type(data)))
            print(data['Login']['username'])
        
        return data    
    
    def save_toml_file(self, filename: pl.Path, toml_object: tomlkit) -> None:
        """Takes python toml object and writes `.toml` file to filesystem

        Parameters
        ----------
        filename : pl.Path
            Path to output file on filesystem
        toml_object : tomlkit
            Python TOML object
        """
        with open(filename, mode='wt', encoding='utf-8') as file:
            tomlkit.dump(toml_object, file)

    def toml_append_password(self, toml_object: tomlkit, pwd: str) -> None:
        """Append password entry und Login table.

        Parameters
        ----------
        toml_object : tomlkit
            Python TOML object.
        pwd : str
            Password for webscraping login
        """
        toml_object['Login'].add("password", pwd) # pylint: disable=no-member
        toml_object['Login']['password'].comment('Input from Password Dialog')