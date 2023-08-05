'''
Tools for manipulating files on operating system level
'''
import datetime as dt
import pathlib as pl
import pandas as pd
# Custom imports
from modules.user import user
from modules import filepersistence
from modules.scrapedata import get_daysum_files

# create user based on config file
User = user()

def pathlib_move(src,dest,appendix):
    '''
    use pathlib to move file, rename file: 'today_appendix.csv'
    src, dest: filetype= pathlib path
    appendix: type string, append to filename
    '''
    path = pl.Path(src)
    new_filename = dest / str(str(dt.date.today().strftime('%Y%m%d') + '_' + str(appendix)) + '.csv')
    path.rename(new_filename)

def move_files(meter_number):
    '''
    copy files to workdir
    rename files

    meter_number: day/night meter device number
    daysum files hardcoded in path_to_raw/workdir variables
    '''

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
    '''
    Create dataframe for data analysis
    workdir: path to csv files
    metertype: either day or night meter
    '''
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
    '''
    Download files from stromnetzgraz and move to work directory
    '''
    filepersistence.initialize_dates_log()
    dates = filepersistence.create_dates_var()

    if not dates['start'] == dt.date.today().strftime('%d-%m-%Y'):                 # scrape just once a day

        get_daysum_files(User.headless_mode)
        move_files(User.day_meter)
        move_files(User.night_meter)
    else:
        print('Most recent data already downloaded')