from SMIT.application import Application

def test_create_app():
    app = Application()
    assert app.Login['username'] != ''
    