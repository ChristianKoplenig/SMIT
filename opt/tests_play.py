# pylint: disable=no-member
# pylint: disable=import-outside-toplevel
import pathlib as pl
import datetime as dt
from collections import namedtuple
import pandas as pd

# Setup
from SMIT.application import Application
app = Application(True)
################################################
# app.persistence.initialize_dates_log()
# dates_loaded = app.persistence.load_dates_log()
# print(dates_loaded)

# dates_new = {**dates_loaded}

# dates_new['last_scrape'] = 'testvar'

# print(f'after: {dates_new}')



# source_dir = pl.Path('./.dummy/csv_raw/daily')
# dest_dir = pl.Path('./.dummy/csv_workdir/daily')

# filename = str(str(dt.date.today().strftime('%Y%m%d') 
#                             + '_' + str(999996)) 
#                             + '.csv')
# f_list = [ ]
# for file in source_dir.glob('*.csv'):
#     f_list.append(file.stem)
    
# print(f'Filename: {f_list}')

# def fh_paths():
#     """Create paths for filehandling tests.

#     Returns
#     -------
#     _type_
#         _description_
#     """
#     Path = namedtuple("Path", ["source_dir",
#                                "dest_dir",
#                                "source_files",
#                                "dest_files",
#                                "filename",
#                                "test_meter"])
#     source_dir = pl.Path('./.dummy/csv_raw/daily')
#     dest_dir = pl.Path('./.dummy/csv_workdir/daily')
#     source_files = [ ]
#     dest_files = [ ]
#     filename = str(str(dt.date.today().strftime('%Y%m%d') 
#                             + '_' + str(199996)))
#     test_meter = app.Meter['day_meter']
#     return Path(source_dir,
#                 dest_dir,
#                 source_files,
#                 dest_files,
#                 filename,
#                 test_meter) 

# Path = fh_paths()    
# print(Path.source_dir)
# app.os_tools.move_files_to_workdir(app.Meter['day_meter'])
# dest_dir = pl.Path('./.dummy/csv_workdir/daily')
# filename = str(str(dt.date.today().strftime('%Y%m%d')
#                    + '_' 
#                    + str(199996)
#                    + '.csv'))
# csv_path = dest_dir / filename

# df = pd.read_csv(csv_path,
#                 sep=';',
#                 decimal=',',
#                 header=0,
#                 parse_dates=['date'],
#                 converters={'date': lambda t: 
#                     dt.datetime.strptime(t,
#                                         '%Y-%m-%dT%H:%M:%S.%f%z').date()},
#                 names=['date',
#                        'zaehlerstand',
#                        '1',
#                        '2',
#                        'verbrauch',
#                        '3',
#                        '4'],
#                 usecols=lambda x: x in ['date', 'zaehlerstand', 'verbrauch'])

# print(df)

