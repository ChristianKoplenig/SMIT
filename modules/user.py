import sys
if sys.version_info < (3, 11):
    import tomli as tomlib
else:
    import tomlib

class user():
    """
    A class that holds all the userdefined data and settings.

    Attributes
    ----------
    Attributes are infered during run time from the TOML config file.

    Methods
    -------
    None
    """

    def __init__(self, file_path : str = './user_data.toml'):
        """
        The constructor reads a TOML config file from *file_path*
        and loops through the dictionary in order to set the attributes
        of the class to self.key = value.

        Parameters
        ----------
        file_path : str, optional
            path to user config file
        """

        # load file
        with open(file_path, 'rb') as file:
            data = tomlib.load(file)

        # loop through all key value pairs of the config file
        # and set them as attributes of the class
        for key, value in data.items():
            setattr(self, key, value)

    def __repr__(self):
        """
        This special function gets called if you use print on a class instance.

        Parameters
        ----------
        None

        Returns
        -------
        str
            Returns a string representation of the class.
        """
        return self.username

if __name__ == '__main__':
    User = user('../user_data.toml')
    print(User.username)
    print(User)
