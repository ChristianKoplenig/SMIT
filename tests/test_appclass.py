# pylint: disable=no-member
import pytest # pylint: disable=import-error
from SMIT.application import Application

@pytest.mark.application
def test_application_username():
    """Test if the app.Login['username'] variable has any attribute.
    """
    app = Application()
    assert app.Login['username'] != ''

@pytest.mark.application
def test_application_module():
    """Test if the app.gui variable has any attribute.
    """
    app = Application()
    assert app.gui != ''
    