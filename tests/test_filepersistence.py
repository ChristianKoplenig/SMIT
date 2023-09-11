"""Test serializing of date object.

---

The application uses a variable called dates to
persist the dates input for the webscraper in between
application runs. This is done via pickling the dates object.
"""
# pylint: disable=no-member
import pathlib as pl
from datetime import date,timedelta
from collections import namedtuple
import pytest # pylint: disable=import-error

from SMIT.application import Application

app = Application(True)

@pytest.fixture
def fp_tests_setup():
    """Fixture for serializing tests.

    - Unpickle the dates object.  
    - Create a dummy and a modified version of the dates object.
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
    """Test the creation of the dates object.

    Assert:
        If the dates pickle object exists on the file system.
    """
    # check dates exist
    assert fp_tests_setup.dates_path.exists
    
@pytest.mark.smoke
@pytest.mark.persistence
def test_load_dates_log(fp_tests_setup):
    """Test unpickling of dates object.
    
    Assert:
        Dates variable from fixture equals dynamically loaded variable.
    """
    
    assert fp_tests_setup.dates_static == fp_tests_setup.dates_loaded
    
@pytest.mark.smoke
@pytest.mark.persistence
def test_modify_dates_log(fp_tests_setup):
    """Test pickling/unpickling methods.
    
    Unpickle, modify and pickle the dates object.
    
    Assert:
        Modified dates variable from fixture 
        equals dynamically modified variable.
    """
    # Prepare modified dates log variable
    dates_write = {**fp_tests_setup.dates_loaded}
    dates_write['last_scrape'] = 'modified'
    # Write modified variable to disk
    app.persistence.save_dates_log(dates_write)
    # Reload the modified variable
    dates_reload = app.persistence.load_dates_log()
    
    assert dates_reload == fp_tests_setup.dates_modified
