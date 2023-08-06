import sys
if sys.version_info < (3, 11):
    import tomli as tomlib
else:
    import tomlib

import pathlib as pl
import tkinter as tk

class user():
    """A class that holds all the userdefined data and settings.

    Attributes
    ----------
    Attributes are infered during run time from the TOML config file.

    Methods
    -------
    None
    """

    def __init__(self,
                 user_path : str = './',
                 user_data_file_name : str = 'user_data.toml',
                 user_settings_file_name_path : str = 'user_settings.toml'):
        """Initialize user

        The constructor reads a TOML config file from *file_path*
        and loops through the dictionary in order to set the attributes
        of the class to self.key = value.

        Parameters
        ----------
        file_path : str, optional
            path to user config file
        """

        # get user data and settings from TOML files
        self.__add_TOML_to_attributes(user_path, user_data_file_name)
        self.__add_TOML_to_attributes(user_path, user_settings_file_name_path)

        # if password is not pressent open a simple gui dialog
        if not hasattr(self, 'password'):
            self.__ask_for_password_and_add_to_attributes()


    def __add_TOML_to_attributes(self, file_path : str, file_name : str):
        # load file
        with open(pl.Path(file_path, file_name), 'rb') as file:
            data = tomlib.load(file)

        # loop through all key value pairs of the config file
        # and set them as attributes of the class
        for key, value in data.items():
            setattr(self, key, value)

    def __ask_for_password_and_add_to_attributes(self):
        root = tk.Tk()
        root.withdraw()
        password = tk.simpledialog.askstring('Please insert password', 'Password:', show='*')
        root.destroy()
        setattr(self, 'password', password)

    def __repr__(self):
        """This special function gets called if you use print on a class instance.

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
    User = user('../')
    print(User.username)
    print(User)
