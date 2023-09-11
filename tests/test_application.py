"""Test the initialization of the core functionalities.
"""
# pylint: disable=no-member
import os
import pytest # pylint: disable=import-error

from SMIT.application import Application

app = Application(True)

@pytest.mark.smoke
@pytest.mark.application
def test_load_user_data():
    """Test import of `user_data.toml`.
    
    This test asserts if the configuration file for the
    user credentials loads correctly.
    
    Assert:
        If login url is correctly assigned to application self variable.
    
    Note:
        During Application.__init__ the configuration
        of user settings is loaded from `.toml` files.
        There are two different configuration files. One 
        holds the settings for the application and the other
        holds the user credentials.
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
        application self variable.
    
    Note:
        During Application.__init__ the configuration
        of user settings is loaded from `.toml` files.
        There are two different configuration files. One 
        holds the settings for the application and the other
        holds the user credentials.
    """
    assert app.Init['csv_startDate'] != ''
    
@pytest.mark.smoke
@pytest.mark.application
def test_load_modules():
    """Test import of modules.
    
    Assert:
        Compare the length of the application instance modules dict
        with static dict.
        
    Note:
        During Application.__init__ each module gets instatiated and
        the instances are stored as objects in a dictionairy with 
        a trivial name as key. 
    """
    modules = dict([
    ('gui', 'UiTools'),
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
        If the Application logger attribute is not `None`
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
    