"""Test the methods for file operations.

---

On application run the files get downloaded to
a raw folder. For further processing the files 
need to be renamed and moved to the work folder.

A method is provided to create a pandas dataframe
with unused columns droped and formatted date fields.
"""
# pylint: disable=no-member
import datetime as dt
import pathlib as pl
from collections import namedtuple
import pytest # pylint: disable=import-error

from SMIT.application import Application

app = Application(True)

@pytest.fixture
def fh_tests_setup():
    """Fixture for file operation tests.

    Load variables from hardcoded paths to create
    a test setup for comparing dynamically loaded variables.
    
    Returns:
        tuple: Static variables for file operation tests.
    """
    Path = namedtuple('Path', ['source_dir',
                               'dest_dir',
                               'source_files',
                               'dest_files',
                               'file_stem',
                               'test_meter',
                               'df_columns',
                               'app'])
    
    source_dir = pl.Path('./.dummy/csv_raw/daily')
    dest_dir = pl.Path('./.dummy/csv_workdir/daily')
    source_files = [ ]
    dest_files = [ ]
    file_stem = str(str(dt.date.today().strftime('%Y%m%d') 
                            + '_' + str(199996)))
    test_meter = app.Meter['day_meter']
    df_columns = ['date', 'zaehlerstand', 'verbrauch', 'rol_med_30', 'rol_med_7']
    
    return Path(source_dir,
                dest_dir,
                source_files,
                dest_files,
                file_stem,
                test_meter,
                df_columns,
                app) 
    
# @pytest.mark.smoke
@pytest.mark.osinterface
def test_move_files(fh_tests_setup):
    """Test move files method.
    
    Assert:
        - If the rename process is handled correctly.  
        - If the file is removed from raw directory.  
    """
    # Run function to test
    app.os_tools._move_files_to_workdir(app.Meter['day_meter'])

    for file in fh_tests_setup.source_dir.glob('*.csv'):
        fh_tests_setup.source_files.append(file.stem) 
            
    for file in fh_tests_setup.dest_dir.glob('*.csv'):
        fh_tests_setup.dest_files.append(file.stem)
    
    # Check move and rename
    for entry in fh_tests_setup.dest_files:
        assert fh_tests_setup.file_stem in entry
        assert fh_tests_setup.test_meter in entry
    # Check if file is removed from source
    for entry in fh_tests_setup.source_files:
        assert fh_tests_setup.test_meter not in entry

@pytest.mark.smoke
@pytest.mark.osinterface
def test_create_dataframe(fh_tests_setup):
    """Test if the dataframe is created correctly.
    
    Assert:
        - Deletion of unused columns.
        - Naming pattern of final pandas dataframe.
    """
  
    df_testfunction = app.os_tools.create_dataframe(
        app.Folder['work_daysum'],
        app.Meter['day_meter'])
    
    # Test if not needed columns get dropped 
    assert len(fh_tests_setup.df_columns) == len(df_testfunction.columns)
    
    # Test if all needed columns exist and are labeled correctly
    for entry in fh_tests_setup.df_columns:
        assert entry in df_testfunction.columns
