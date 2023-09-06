# pylint: disable=no-member
import os
import pytest # pylint: disable=import-error
from SMIT.application import Application

app = Application(True)

@pytest.mark.smoke
@pytest.mark.application
def test_load_user_data():
    """Test import of `user_data.toml`.
    
    See if the config file for user credentials loads.
    """
    assert app.Login['username'] != ''

@pytest.mark.smoke
@pytest.mark.application
def test_load_user_settings():
    """Test import of `user_settings.toml`.
    
    See if the config file for user settings loads.
    """
    assert app.Init['csv_startDate'] != ''
    
@pytest.mark.smoke
@pytest.mark.application
def test_load_modules():
    """Test import of modules.
    
    Compares the length of the app instance with static dict.
    """
    modules = dict([
    ('gui', 'UiTools'),
    ('rsa', 'RsaTools'),
    ('toml_tools', 'TomlTools'),
    ('os_tools', 'OsInterface'),
    ('persistence', 'Persistence'),
    ('scrape', 'Webscraper')])
    
    test_modules = app._load_modules()
    
    assert len(test_modules) == len(modules)
    
@pytest.mark.smoke
@pytest.mark.application
def test_logger():
    """Test if the logger module is loaded
    """
    assert app.logger != ''
    
@pytest.mark.smoke
@pytest.mark.application
def test_folderstructure():
    """Test if all folders exist
    """
    for folder_path in app.Folder.values():
        assert os.path.exists(folder_path)
    