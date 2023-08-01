import datetime as dt
import pathlib as pl
import user_class

# create user class
User = user_class.create_user()

def pathlib_move(src,dest,appendix):
    '''
    use pathlib to move file
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


#move_files(User.day_meter)