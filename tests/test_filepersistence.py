# pylint: disable=no-member
#import pickle
import pathlib as pl
from datetime import date,timedelta
import pytest # pylint: disable=import-error
from collections import namedtuple
from SMIT.application import Application

app = Application(True)

@pytest.fixture
def fp_tests_setup():
    """Persistence tests setup

    Returns
    -------
    _type_
        _description_
    """
    setup = namedtuple('test_setup', ['dates_path',
                                      'dates_loaded',
                                      'dates_static',
                                      'dates_modified'])
    
    dates_path = pl.Path(app.Path['persist_dates'])
    
    # Call creation of dates.pkl file
    app.persistence.initialize_dates_log()
    # Load dates log variable
    dates_loaded = app.persistence.load_dates_log()
    
    # Dates test variable
    dates_static = dict()
    dates_static['start'] = app.Init['csv_startDate']
    dates_static['end'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
    dates_static['last_scrape'] = 'never'
    
    # Modified test variable
    dates_modified = dict()
    dates_modified['start'] = app.Init['csv_startDate']
    dates_modified['end'] = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
    dates_modified['last_scrape'] = 'modified'

    return setup(dates_path, dates_loaded, dates_static, dates_modified)



@pytest.mark.smoke
@pytest.mark.persistence
def test_init_dates_log(fp_tests_setup):
    """Variable for date peristence exist
    
    Check `SMIT.filepersistence.Persistence.initialize_dates_log()`

    Parameters
    ----------
    fp_tests_setup : _type_
        _description_
    """
    # check dates exist
    assert fp_tests_setup.dates_path.exists
    
@pytest.mark.smoke
@pytest.mark.persistence
def test_load_dates_log(fp_tests_setup):
    """Dates logging correctly loaded

    Parameters
    ----------
    fp_tests_setup : _type_
        _description_
    """
    
    assert fp_tests_setup.dates_static == fp_tests_setup.dates_loaded
    
@pytest.mark.smoke
@pytest.mark.persistence
def test_modify_dates_log(fp_tests_setup):
    """Dates logging routine
    
    Load variable, modify variable, save variabel.
    Reload safed variable

    Parameters
    ----------
    fp_tests_setup : _type_
        _description_
    """
    # Prepare modified dates log variable
    dates_write = {**fp_tests_setup.dates_loaded}
    dates_write['last_scrape'] = 'modified'
    # Write modified variable to disk
    app.persistence.save_dates_log(dates_write)
    # Reload the modified variable
    dates_reload = app.persistence.load_dates_log()
    
    assert dates_reload == fp_tests_setup.dates_modified
    
    