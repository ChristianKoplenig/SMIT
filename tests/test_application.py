"""Test the initialization of the core functionalities.

---

Application Class __init__:
---------------------------
The configuration of user settings is loaded from `.toml` files.  
There are two different configuration files.
One holds the __settings__ for the application and the other
holds the user __credentials__.

Each module instance is stored as a object in a dictionary
with a trivial name as key.

The existing folder structure is checked against the folders
defined in the settings file and if the folders do not exist 
they are created. 
"""
# pylint: disable=no-member
import os
import pytest # pylint: disable=import-error

from smit.application import Application

app = Application(True)

@pytest.mark.smoke
@pytest.mark.application
def test_load_user_data():
    """Test import of `user_data.toml`.
    
    This test asserts if the configuration file for the
    user credentials loads correctly.
    
    Assert:
        If login url is correctly assigned to application attribute variable.
    """
    assert app.Login['url'] == 'https://webportal.stromnetz-graz.at/login'

@pytest.mark.smoke
@pytest.mark.application
def test_load_user_settings():
    """Test import of `user_settings.toml`.
    
    This test asserts if the configuration file for the
    user settings loads correctly.
    
    Assert:
        If start date for initial run is correctly assigned to 
        application attribute variable.
    """
    assert app.Init['csv_startDate'] != ''
    
@pytest.mark.smoke
@pytest.mark.application
def test_load_modules():
    """Test import of modules.
    
    Assert:
        Compare the length of the application instance modules dict
        with a static dict.
    """
    modules = dict([
    ('rsa', 'RsaTools'),
    ('toml_tools', 'TomlTools'),
    ('os_tools', 'OsInterface'),
    ('persistence', 'Persistence'),
    ('scrape', 'Webscraper')])
    
    app_modules = app._load_modules()
    
    assert len(app_modules) == len(modules)
    
@pytest.mark.smoke
@pytest.mark.application
def test_logger():
    """Test initialization of the logger module.
    
    Assert:
        If the Application logger attribute is __not__ `None`
    """
    assert app.logger != ''
    
@pytest.mark.smoke
@pytest.mark.application
def test_folderstructure():
    """Test if all folders exist.
    
    Assert:
        If all folders from `user_settings.toml` folders table
        do exist in the application folder.
    """
    for folder_path in app.Folder.values():
        assert os.path.exists(folder_path)
    