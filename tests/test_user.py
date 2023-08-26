from SMIT.user import user

def test_user_has_name():
    user_instance = user()  # Create user from user_data file
    assert user_instance.Login['username'] != ''