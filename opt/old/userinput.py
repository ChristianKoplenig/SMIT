"""GUI

---
`UiTools`
---------

- Get user credentials.
- Get day and night meter numbers.
- Option to permanently store password in settings.

Typical usage:

    app = Application()
    app.gui.method()
"""
import sys
import tkinter as tk
from tkinter import ttk
import pathlib as pl
import base64
# Type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from SMIT.application import Application


class UiTools():
    """Use tkinter library for user input.

    ---
    
    Start a gui dialog for getting
    user infomation and provide the option to save
    the password in the config file.
    
    Attributes:
        app (class): Accepts `SMIT.application.Application` type attribute.
    """
    def __init__(self, app: 'Application') -> None:

        self.user = app
        self.logger = app.logger
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)
        
        self.user_data_path = pl.Path(self.user.Path['user_data'])

        # Tkinter setup
        self.window = None
        # Tkinter widgets
        self.button_confirm = None
        self.button_close = None
        self.button_delPwd = None
        self.checkbox_savePwd = None
        self.entry_password = None
        self.entry_username = None
        self.entry_meter_day = None
        self.entry_meter_night = None
        # Tkinter variables
        self.var_password = None
        self.save_credentials = None

        # Logger setup
        self.logger = app.logger
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)

    def _def_variables(self) -> None:
        """Assign tkinter classes to variables.
        
        After declaring the classes all variables
        are populated with the data from user settings.
        This is done to prefill the gui and give the user
        the possibility to alter the data from the settings.
        
        Note:
            This is done in a method to avoid
            calling the tkinter library during init.
        """
        self.var_password = tk.StringVar()
        self.save_credentials = tk.BooleanVar()
        self.entry_username = tk.StringVar()
        self.entry_meter_day = tk.StringVar()
        self.entry_meter_night = tk.StringVar()

        # Assign Values from config to entry fields
        self.entry_username.set(self.user.Login['username'])
        self.entry_meter_day.set(self.user.Meter['day_meter'])
        self.entry_meter_night.set(self.user.Meter['night_meter'])

        if 'password' in self.user.Login:
            pwd_b64dec = base64.b64decode(self.user.Login['password'])
            self.var_password.set(
                self.user.rsa.decrypt_pwd(pwd_b64dec)
            )

    def _dev_widgets(self) -> None:
        """Configure the gui widgets.
        
        Note:
            This is done in a method to avoid
            calling the tkinter library during init.
        """
        self.button_confirm = tk.Button(
            text='Confirm',
            command=self._button_accept
        )

        self.button_close = tk.Button(
            text='Close window',
            command=self._button_close
        )
        
        self.button_delPwd = tk.Button(
            text='Delete stored password',
            command=self._button_delpwd
        )

        self.checkbox_savePwd = ttk.Checkbutton(
            text='Save user credentials in user_data',
            variable=self.save_credentials
        )

        self.entry_password = tk.Entry(
            fg='yellow',
            bg='blue',
            textvariable=self.var_password,
            show='*'
        )
        
        self.entry_username = tk.Entry(
            textvariable=self.entry_username
        )
        
        self.entry_meter_day = tk.Entry(
            textvariable=self.entry_meter_day
        )
        
        self.entry_meter_night = tk.Entry(
            textvariable=self.entry_meter_night
        )

    def _return_pressed(self, event: None) -> None:
        """Helper function for key binding.

        Args:
            event (None): Placeholder
        """
        self._button_accept()

    def _text(self, txt_input: str) -> None:
        """Create generic text widget.

        Args:
            txt_input (string): Text to show in gui window.
        """
        text = tk.Label(
            text=txt_input,
            height=3
        )
        text.pack()

    def _button_accept(self) -> None:
        """Define accept button action.

        If the "Save user credentials..." checkbox is activated then the 
        entered data will be added to the `user_data.toml` file 
        and the user instance.  
        Else everything entered will be added to the active user instance and
        won't get stored in a file.
        """
        # Encrypt credentials with rsa keys
        pwd_enc = self.user.rsa.encrypt_pwd(self.var_password.get())
        # Convert password to str representation for storing it in `user_data.toml`
        pwd_str = base64.b64encode(pwd_enc).decode('utf-8')

        save_credentials_activated = self.save_credentials.get()

        if save_credentials_activated:

            # Append credentials to user_data.toml
            self.user.toml_tools.add_entry_to_config(self.user_data_path,
                                                     'Login',
                                                     'password',
                                                     pwd_str)
            self.user.toml_tools.add_entry_to_config(self.user_data_path,
                                                     'Login',
                                                     'username',
                                                     self.entry_username.get())
            self.user.toml_tools.add_entry_to_config(self.user_data_path,
                                                     'Meter',
                                                     'day_meter',
                                                     self.entry_meter_day.get())
            self.user.toml_tools.add_entry_to_config(self.user_data_path,
                                                     'Meter',
                                                     'night_meter',
                                                     self.entry_meter_night.get())
            # Make credentials available in user instance
            self.user.Login['username'] = self.entry_username.get()
            self.user.Login['password'] = pwd_str
            self.user.Meter['day_meter'] = self.entry_meter_day.get()
            self.user.Meter['night_meter'] = self.entry_meter_night.get()
            self.logger.debug('Credentials permanently added to user data')

        else:
            # Temporary store credentials in user instance
            self.user.Login['username'] = self.entry_username.get()
            self.user.Login['password'] = pwd_str
            self.user.Meter['day_meter'] = self.entry_meter_day.get()
            self.user.Meter['night_meter'] = self.entry_meter_night.get()
            self.logger.debug('Credentials temporarily added to user attributes')

        self.window.destroy()

    def _button_delpwd(self) -> None:
        """Delete password entry from user configuration.

        The stored password will be deleted from the user config
        and the user instance attributes.
        """
        if 'password' in self.user.Login:
            del self.user.Login['password']
            self.user.toml_tools.delete_entry_from_config(self.user_data_path,
                                                          'Login',
                                                          'password')
            self.var_password.set('')
        else:
            self.var_password.set('')

    def _button_close(self) -> None:
        """Define close button action.
        
        On button press the window will be closed.
        
        Note:
            This raises a ugly error message when executed in
            a Jupyter Notebook setup. To my knowledge the 
            sys.exit() command is needed because the init of
            the application should be stopped. 
        """
        self.window.destroy()
        sys.exit('Close button pressed')
    
    def _window_setup(self) -> None:
        """Define entries for "User credentials" dialog.
        
        Manage the widgets for the top level window.
        """
        self._text('Enter username')
        self.entry_username.pack()
        self._text('Enter your "Stromnetz Graz" password')
        self.entry_password.pack()
        self.entry_password.focus()
        self._text('Please read the disclaimer for details on password handling')
        self._text('Select Meters (last six digits)')
        self._text('Day')
        self.entry_meter_day.pack()
        self._text('Night')
        self.entry_meter_night.pack()
        self.checkbox_savePwd.pack()
        self._text('')
        self.button_delPwd.pack()
        self.button_confirm.pack()
        self.button_close.pack()

    def credentials_dialog(self) -> None:
        """Built top level window.
        
        Call a top level widget and populate it
        with all needed widgets for 
        the "User credentials" dialog.
        """
        self.window = tk.Tk()
        self.window.title('User credentials')
        self.window.geometry('400x655')
        self.window.bind('<Return>', self._return_pressed)

        self._def_variables()
        self._dev_widgets()
        self._window_setup()

        self.window.mainloop()

    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"


# Pdoc config get underscore methods
__pdoc__ = {name: True
            for name, classes in globals().items()
            if name.startswith('_') and isinstance(classes, type)}


__pdoc__.update({f'{name}.{member}': True
                 for name, classes in globals().items()
                 if isinstance(classes, type)
                 for member in classes.__dict__.keys()
                 if member not in {'__module__', '__dict__',
                                   '__weakref__', '__doc__'}})

__pdoc__.update({f'{name}.{member}': False
                 for name, classes in globals().items()
                 if isinstance(classes, type)
                 for member in classes.__dict__.keys()
                 if member.__contains__('__') and member not in {'__module__', '__dict__',
                                                                 '__weakref__', '__doc__'}})
