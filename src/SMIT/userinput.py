"""
Tools for handling the password input/storing dialog
"""
import tkinter as tk
from tkinter import ttk
import pathlib as pl
import base64
# Type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from SMIT.application import Application

class UiTools():
    """Tools for interacting with the tkinter library.

    Attributes:
    -----------
    app : class instance
        Hold user information

    Methods
    -------
    _text(txt_input):
        Generates text widget
    _checkbox_save_pwd():
        Generates the save password checkbox.
    _button_accept():
        Reads input from entry field, handles pwd routine.
    password_dialog():
        Routine for getting the user input
    """
    def __init__(self, app: 'Application') -> None:
        """Initialize class with all attributes from user config files.

        Parameters
        ----------
        app : class instance
            Holds the configuration data for program run.
        """
        self.user = app
        
        # Tkinter setup
        self.window = None
        # Tkinter widgets
        self.button_confirm = None
        self.checkbox_savePwd = None
        self.entry_pwd = None
        # Tkinter variables
        self.pwd_entry = None
        self.save_password = None
        
        # Logger setup
        self.logger = app.logger
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)

    def _dev_widgets(self) -> None:
        """Assign widgets to self.
        """
        self.button_confirm = tk.Button(
            text = 'Confirm',
            command= self._button_accept
        )

        self.checkbox_savePwd = ttk.Checkbutton(
            text= 'Save encrypted password in user_data',
            variable= self.save_password
        )

        self.entry_pwd = tk.Entry(
            fg='yellow',
            bg='blue',
            textvariable= self.pwd_entry,
            show= '*'
        )

    def _def_variables(self) -> None:
        """Assign variables to self.
        """
        self.pwd_entry = tk.StringVar()
        self.save_password = tk.BooleanVar()

    def _text(self, txt_input: str) -> None:
        """Create text widget

        Parameters
        ----------
        txt_input : str
            Text to show
        """
        text = tk.Label(
            text= txt_input,
            height=3
        )
        text.pack()

    def _button_accept(self) -> None:
        """Defines what to todo when accept button is pressed.

        If the "save password" checkbox is activated then the password
        will be added to the `user_data.toml` file and the user instance.
        Else the password will be added just to the user instance.
        """
        #Encrypt password with rsa keys
        pwd_enc = self.user.rsa.encrypt_pwd(self.pwd_entry.get())
        # Convert password to str representation for storing it in `user_data.toml`
        pwd_str = base64.b64encode(pwd_enc).decode('utf-8')

        user_data_path = pl.Path(self.user.Path['user_data'])
        save_pwd_activated = self.save_password.get()

        if save_pwd_activated:

            # Append password to user_data.toml
            self.user.toml_tools.add_password_to_toml(user_data_path, pwd_str)
            # Make password available in user instance
            self.user.Login['password'] = pwd_str
            self.logger.debug('Password permanently added to user data')

        else:
            # Temporary store password in user instance
            self.user.Login['password'] = pwd_str
            self.logger.debug('Password temporarily added to user attributes')

        self.window.destroy()

    def _window_setup(self) -> None:
        self._text('Please enter your Stromnetz Graz password')
        self.entry_pwd.pack()
        self.entry_pwd.focus()
        self.checkbox_savePwd.pack()
        self.button_confirm.pack()
        self._text('Please read the disclaimer for details on password handling')

    def password_dialog(self) -> None:
        """Initiate "Enter Password" dialog.
        """
        self.window = tk.Tk()
        self.window.title('Password Dialog')
        self.window.geometry('400x200')

        self._def_variables()
        self._dev_widgets()
        self._window_setup()

        self.window.mainloop()

    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"