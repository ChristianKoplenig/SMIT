from datetime import date
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
    
    #### User Input
    path_to_raw = os.path.abspath(user_data.csv_dl_daysum)
    workdir = os.path.abspath(user_data.csv_wd_daysum)
    
    # set path to workdir
    os.chdir(workdir)
    workdir_files = glob.glob('*.csv')
    
    # set path to raw files
    os.chdir(path_to_raw)
    raw_files = glob.glob('*.csv')
    
    ### beginn iteration over files ###
    
    # select files in raw folder
    for filename in raw_files:
        
        #filter for input files
        if meter_number in filename:
        
        ### copy ###
        
        #path for shutil copy
            os.chdir(path_to_raw)
            src = pl.Path(filename).absolute()
            dest = workdir
            
            #check if imported
            if filename in workdir_files:
                print('no new files')
                #pass
                
            else:
                
                #copy files
                shutil.copy(src, dest)
                                
                # ### modify ###
            
                # #switch to workdir
                # os.chdir(workdir)
            
                # #read and modify csv file
                # save_file = str(date.today().strftime('%Y%m%d') + '_' + str(meter_number)) + '.csv'
                # os.rename(filename,save_file)
                # print('files added')
                # #print copy message
                # #print('added file: ', filename)
    #return() 
 
meter_number = user_data.day_meter   
#save_file = str(date.today().strftime('%Y%m%d') + '_' + str(meter_number))
move_files(meter_number)
#print(workdir_files)