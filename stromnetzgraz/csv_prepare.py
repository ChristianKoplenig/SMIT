'''
prepare the workdir files
'''
import glob
import os
import shutil
import pathlib as pl
import pandas as pd

def csv_import():
    '''
    copies files to workdir, adds measurement column, formats timestamp column
    '''
    
    #### User Input
    search = ("Tagstrom")           #search criteria for filename
    path_to_raw = r'/media/data/coding/strom/stromnetzgraz/csv_raw'
    workdir = r'/media/data/coding/strom/stromnetzgraz/csv'
    
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
        if search in filename:
        
        ### copy ###
        
        #path for shutil copy
            os.chdir(path_to_raw)
            src = pl.Path(filename).absolute()
            dest = workdir
            
            #check if imported
            if filename in workdir_files:
                
                pass
                
            else:
                
                #copy files
                shutil.copy(src, dest)
                                
                ### modify ###
            
                #switch to workdir
                os.chdir(workdir)
            
                #read and modify csv file
                file = filename
                df = pd.read_csv(file)
                #df.drop('index', axis=1, inplace=True)
                #df['Measurement'] = file[0:-13]
                #df['Ablesezeitpunkt'] = pd.to_datetime(df['Ablesezeitpunkt'], unit='ms', utc=True, yearfirst=True)
                df.to_csv(file)
                
                #print copy message
                print('added file: ', filename)
    return() 
