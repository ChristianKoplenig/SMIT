"""Get and show user credentials.

---

- Create and arrange label widgets  
- Create and arrange entry widgets   

Typical usage:

    windowframe = ButtonFrame()
"""
import tkinter as tk
import base64
import customtkinter as ctk


class CredentialsFrame(ctk.CTkFrame):
    """Credentials setup for SMIT Gui

    - Setup entries for entry widgets
    - Decrypt password from `user_data.toml`
    - Create and arrange label widgets
    - Create and arrange entry widgets
    - Update password entry widget

    Returns:  

    """
    def __init__(self, master):
        super().__init__(master)

        self.title = ctk.CTkLabel(
            self,
            text='User Credentials')
        self.title.grid(row=0, padx=10, pady=(0,20), sticky='ew', columnspan=2)

        # Initialize textvariables
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
            ##### debugging
            #self.password.set(master.user.Login['password'])

        # Labels
        self.username_lbl = ctk.CTkLabel(
            self,
            text='Username: ')
        self.username_lbl.grid(row=1, column=0, padx=20, pady=5)

        self.daymeter_lbl = ctk.CTkLabel(
            self,
            text='Day meter: ')
        self.daymeter_lbl.grid(row=2, column=0, padx=20, pady=5)

        self.nightmeter_lbl = ctk.CTkLabel(
            self,
            text='Night meter: ')
        self.nightmeter_lbl.grid(row=3, column=0, padx=20, pady=5)

        self.password_lbl = ctk.CTkLabel(
            self,
            text='Password: ')
        self.password_lbl.grid(row=4, column=0, padx=20, pady=5)

        # Entries
        self.entry_username = ctk.CTkEntry(
            self,
            textvariable=self.username,
            width=250)
        self.entry_username.grid(row=1, column=1, padx=(20, 20), pady=5)

        self.entry_daymeter = ctk.CTkEntry(
            self,
            textvariable=self.day_meter,
            width=70)
        self.entry_daymeter.grid(row=2, column=1, padx=(20, 20), pady=5, sticky='w')

        self.entry_nightmeter = ctk.CTkEntry(
            self,
            textvariable=self.night_meter,
            width=70)
        self.entry_nightmeter.grid(row=3, column=1, padx=(20, 20), pady=5, sticky='w')

        self.entry_password = ctk.CTkEntry(
            self,
            textvariable=self.password,
            width=250,
            show='*')
        self.entry_password.grid(row=4, column=1, padx=(20, 20), pady=5, sticky='w')

    def update_pwd_entry(self,new_entry) -> None:
        """Update from outside credentials class

        Args:
            new_entry (string): new password entry
        """
        self.password.set(new_entry)

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