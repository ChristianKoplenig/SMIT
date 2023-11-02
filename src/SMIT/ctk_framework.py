"""GUI

---
'Custom TKinter Framework`
-------------------------

- Main entry point for the application.

Typical usage:
    On startup
"""
import customtkinter
import tkinter as tk
import pathlib as pl
import base64

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from SMIT.application import Application

### Developement imports
from SMIT.application import Application


class CredentialsFrame(customtkinter.CTkFrame):
    """Frame for credentials

    """
    def __init__(self, master):
        super().__init__(master)

        self.title = customtkinter.CTkLabel(
            self,
            text='User Credentials')
        self.title.grid(row=0, padx=10, pady=(10,20), sticky='ew', columnspan=2)

        # Initialize empty entries
        self.username = tk.StringVar(value=master.user.Login['username'])
        self.day_meter = tk.StringVar(value=master.user.Meter['day_meter'])
        self.night_meter = tk.StringVar(value=master.user.Meter['night_meter'])
        self.password = tk.StringVar()

        # Read saved password
        if 'password' in master.user.Login:
            pwd_b64dec = base64.b64decode(master.user.Login['password'])
            self.password.set(
                master.user.rsa.decrypt_pwd(pwd_b64dec)
            )

        # Labels
        self.username_lbl = customtkinter.CTkLabel(
            self,
            text='Username: ')
        self.username_lbl.grid(row=1, column=0, padx=20, pady=5)

        self.daymeter_lbl = customtkinter.CTkLabel(
            self,
            text='Day meter: ')
        self.daymeter_lbl.grid(row=2, column=0, padx=20, pady=5)

        self.nightmeter_lbl = customtkinter.CTkLabel(
            self,
            text='Night meter: ')
        self.nightmeter_lbl.grid(row=3, column=0, padx=20, pady=5)

        self.password_lbl = customtkinter.CTkLabel(
            self,
            text='Password: ')
        self.password_lbl.grid(row=4, column=0, padx=20, pady=5)


        # Entries
        self.username_conf = customtkinter.CTkEntry(
            self,
            textvariable=self.username,
            width=250)
        self.username_conf.grid(row=1, column=1, padx=(20, 20), pady=5)

        self.daymeter_conf = customtkinter.CTkEntry(
            self,
            textvariable=self.day_meter,
            width=70)
        self.daymeter_conf.grid(row=2, column=1, padx=(20, 20), pady=5, sticky='w')

        self.nightmeter_conf = customtkinter.CTkEntry(
            self,
            textvariable=self.night_meter,
            width=70)
        self.nightmeter_conf.grid(row=3, column=1, padx=(20, 20), pady=5, sticky='w')

        self.password_conf = customtkinter.CTkEntry(
            self,
            textvariable=self.password,
            width=250,
            show='*')
        self.password_conf.grid(row=4, column=1, padx=(20, 20), pady=5, sticky='w')

class ButtonFrame(customtkinter.CTkFrame):
    """Frame for buttons

    Args:
        customtkinter (_type_): _description_

    Returns:
        _type_: _description_
    """
    def __init__(self, master):
        super().__init__(master)

        # self.button_close = customtkinter.CTkButton(
        #     #master=AppGui,
        #     text='Close Window',
        #     command=print('hello')
        # )
        # self.button_close.grid(row=0, column=0)        


class AppGui(customtkinter.CTk):
    """Main GUI class

    ---

    Use as entry point.
    Generate main application window.

    Args:
        customtkinter (_type_): _description_
    """


    def __init__(self, app: 'Application') -> None:
        super().__init__()

        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("dark")

        self.user = app
        self.user_data_path = pl.Path(self.user.Path['user_data'])

        # Logger setup
        self.logger = app.logger
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)

        # Main window
        self.title("SMIT")
        self.geometry("1440x900")
        self.grid_columnconfigure(0, weight=1)
        #self.grid_rowconfigure(0, weight=1)

        # Frames
        self.credentials_frame = CredentialsFrame(self)
        self.credentials_frame.grid(row=0, column=0, sticky='w')

        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=0,column=1)

    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"
    

user = Application()
ctk = AppGui(user)
ctk.mainloop()

















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