import datetime as dt
import glob
import os
import shutil
import pathlib as pl
import pandas as pd
import user_data

def move_files(meter_number):
    '''
    copy files to workdir
    rename files
    
    meter_number: day/night meter device number
    daysum files hardcoded in path_to_raw/workdir variables
    '''
    
    # set path variables
    path_to_raw = pl.Path(user_data.csv_dl_daysum).absolute()
    workdir = pl.Path(user_data.csv_wd_daysum).absolute()
    
    # # set path to raw files
    # os.chdir(path_to_raw)
    # raw_files = glob.glob('*.csv')
    
    ### beginn iteration over files ###
    
    # select files in raw folder
    for filename in path_to_raw.glob('*.csv'):
        
        filename_cdate = filename.stat().st_ctime
        cdate = dt.datetime.fromtimestamp(filename_cdate).strftime('%Y-%m-%d')
        # just process downloaded files from today
        if cdate == dt.date.today().strftime('%Y-%m-%d'):
        #filter for input files
            if meter_number in str(filename):
            
            ### copy ###

            #path for shutil copy
                os.chdir(path_to_raw)
                src = pl.Path(filename).absolute()
                dest = workdir


                #copy files
                shutil.copy(src, dest)

                ### modify ###

                #switch to workdir
                os.chdir(workdir)

                #change filename
                save_file = str(dt.date.today().strftime('%Y%m%d') + '_' + str(meter_number)) + '.csv'
                os.rename(filename,save_file)
                print('files added')
 
#save_file = str(date.today().strftime('%Y%m%d') + '_' + str(meter_number))
move_files(user_data.day_meter)
#print(workdir_files)