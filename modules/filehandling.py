"""
    Tools for manipulating files on os basis
"""
import datetime as dt
import pathlib as pl
import pandas as pd
# Custom imports
from modules import dynamicclass
from modules import filepersistence
from modules.scrapedata import get_daysum_files

# create user class
User = dynamicclass.create_user()

def pathlib_move(src,dest,appendix):
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
        
def move_files(meter_number):
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
    path_to_raw = pl.Path(User.csv_dl_daysum).absolute()
    workdir = pl.Path(User.csv_wd_daysum).absolute()

    # select files in raw folder
    for filename in path_to_raw.glob('*.csv'): 
        filename_cdate = filename.stat().st_ctime
        cdate = dt.datetime.fromtimestamp(filename_cdate).strftime('%Y-%m-%d')
        
        # just process downloaded files from today
        if cdate == dt.date.today().strftime('%Y-%m-%d'):
        
            #filter for input files
            if meter_number in str(filename):
                pathlib_move(filename, workdir, meter_number)
                
def create_dataframe(workdir, metertype):
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
    filelist = []

    for filename in path.glob('*.csv'):
        if (str(metertype) in filename.name):
            filelist.append(filename)
            df_return = pd.concat((pd.read_csv(r,
                                              sep=';',
                                              decimal=',',
                                              header=0,
                                              parse_dates=['date'],
                                              converters={'date': lambda t: dt.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%f%z').date()},
                                              names=['date', 'zaehlerstand', '1', '2', 'verbrauch', '3', '4'],
                                              usecols=lambda x: x in ['date', 'zaehlerstand', 'verbrauch'],
                                            )
                                for r in filelist))

            df_return['zaehlerstand'] = df_return['zaehlerstand'].astype(float)
            df_return['verbrauch'] = df_return['verbrauch'].astype(float)
            df_return.sort_values(by='date', inplace=True)
            df_return.reset_index(drop=True, inplace=True)
            df_return.drop_duplicates(subset='date', keep='first', inplace=True)
    return df_return

def scrapandmove():
    """    
    Download files from stromnetzgraz and move to work directory
    """
    filepersistence.initialize_dates_log()
    dates = filepersistence.create_dates_var()
   
    if not dates['start'] == dt.date.today().strftime('%d-%m-%Y'):                 # scrape just once a day
    
        get_daysum_files(User.headless_mode)
        move_files(User.day_meter)
        move_files(User.night_meter)
    else:
        print('Most recent data already downloaded')