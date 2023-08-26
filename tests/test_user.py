from SMIT.user import user

def test_user_has_name():
    user_instance = user()  # Create user from user_data file
    assert user_instance.Login['username'] != ''
    
def test_print_user_prints_username(capfd):
    user_instance = user()  # Create user from user_data file
    print(user_instance)
    out, err = capfd.readouterr()
    assert user_instance.Login['username'] == out.strip()