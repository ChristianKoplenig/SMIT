import sys
if sys.version_info < (3, 11):
    import tomli as tomlib
else:
    import tomlib

def create_user(file_path : str = './user_data.toml') -> dict:
    """
    Reads a toml config file from *file_path* and returns it as a dictionary.

    Parameters
    ----------
    file_path : str
        path to user config file

    Returns
    -------
    user : dict
        holds key-value pairs of user data
    """
    with open(file_path, 'rb') as config_file:
        user = tomlib.load(config_file)
    return user


if __name__ == '__main__':
    user = create_user('../user_data.toml')
    print(user['username'])
