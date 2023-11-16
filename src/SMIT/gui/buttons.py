"""Application and credentials Buttons

----

- Create and arrange button widgets
- Functions for button commands

Typical usage:

    windowframe = ButtonFrame()
"""
import customtkinter as ctk
import base64

from numpy import mask_indices

class ButtonFrame(ctk.CTkFrame):
    """Buttons setup for SMIT Gui.

    - Setup label
    - Create buttons
    - Arrange buttons
    - Define button commands

    Attributes:

        `ctk.CTkFrame`  

    Returns:

      
    """
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.title = ctk.CTkLabel(
            self,
            text='Buttons')
        self.title.grid(row=0, padx=10, pady=(50,20), sticky='ew')
    
        self.button_close = ctk.CTkButton(
            master=self,
            text='Close Application',
            command=self._button_close
        )
        self.button_close.grid(row=1, padx=10, pady=20)

        self.button_delpwd = ctk.CTkButton(
            master=self,
            text='Delete Password',
            command=self._button_delpwd
        )
        self.button_delpwd.grid(row=2, padx=10, pady=20)

        self.button_savecred = ctk.CTkButton(
            master=self,
            text='Confirm new credentials',
            command=self._button_savecred
        )
        self.button_savecred.grid(row=3, padx=10, pady=20)

        self.button_scrapemove = ctk.CTkButton(
            master=self,
            text='Update data',
            command=self._button_update_data
        )
        self.button_scrapemove.grid(row=1, column=1, padx=10, pady=20)

        self.button_dummy = ctk.CTkButton(
            master=self,
            text='Dummy',
            command=self._button_dummy
        )
        self.button_dummy.grid(row=2, column=1, padx=10, pady=20)

    def _button_update_data(self) -> None:
        """Srape data, reload plots.
        """
        self.master.logger.debug('Data update initialized')
        self.master.user.os_tools.sng_scrape_and_move()
        self.master.reload_plots()

    def _button_close(self) -> None:
        """Close root window.
        """
        self.master.logger.info('All windows closed on button press')
        self.quit()

    def _button_dummy(self) -> None:
        """Call dummy function from root frame
        """
        self.master.initiate_dummy()

    def _button_delpwd(self) -> None:
        """Delete password entry from user configuration.

        The stored password will be deleted from the user config
        and the user instance attributes.
        """
        self.master.credentials_frame.update_pwd_entry('')

        if 'password' in self.master.user.Login:
            
            del self.master.user.Login['password']

            self.master.user.toml_tools.delete_entry_from_config(
                self.master.user_data_path,
                'Login',
                'password')
        self.master.logger.info('Password removed from application instance and config file')
            
    def _button_savecred(self) -> None:
        """Define confirm credentials button action.

        If the "Save credentials" checkbox is activated then the 
        entered data will be added to the `user_data.toml` file 
        and the user instance.  
        Else everything entered will be added to the active user instance and
        won't get stored in a file.
        """
        #Encrypt credentials with rsa keys
        pwd_enc = self.master.user.rsa.encrypt_pwd(
            self.master.credentials_frame.entry_password.get())
        # Convert password to str representation for storing it in `user_data.toml`
        pwd_str = base64.b64encode(pwd_enc).decode('utf-8')

        save_credentials_activated = self.master.checkbox_frame.save_credentials.get()

        #if self.master.checkbox_frame.save_credentials.get() == 'on':
        if save_credentials_activated:

            self.master.checkbox_frame.save_credentials_chkbx.deselect()

            # Append credentials to user_data.toml
            if not 'password' in self.master.user.Login:
                self.master.user.toml_tools.add_entry_to_config(
                    self.master.user_data_path,
                    'Login',
                    'password',
                    pwd_str)
                self.master.logger.info('New password added to config file')
                
            elif self.master.credentials_frame.entry_password.get() == self.master.user.rsa.decrypt_pwd(
                base64.b64decode(self.master.user.Login['password'])):
                self.master.logger.debug('Password not changed')

            else:
                self.master.user.toml_tools.add_entry_to_config(
                    self.master.user_data_path,
                    'Login',
                    'password',
                    pwd_str)
                self.master.logger.info('New password added to config file')
            
            if self.master.user.Login['username'] == self.master.credentials_frame.entry_username.get():
                self.master.logger.debug('User not changed')
            else:
                self.master.user.toml_tools.add_entry_to_config(
                    self.master.user_data_path,
                    'Login',
                    'username',
                    self.master.credentials_frame.entry_username.get())
                self.master.logger.info('New username added to config')
                
            if self.master.user.Meter['day_meter'] == self.master.credentials_frame.entry_daymeter.get():
                self.master.logger.debug('Day meter number not changed')
            else:            
                self.master.user.toml_tools.add_entry_to_config(
                    self.master.user_data_path,
                    'Meter',
                    'day_meter',
                    self.master.credentials_frame.entry_daymeter.get())
                self.master.logger.info('New day meter number added to config')

            if self.master.user.Meter['night_meter'] == self.master.credentials_frame.entry_nightmeter.get():
                self.master.logger.debug('Night meter number not changed')
            else:            
                self.master.user.toml_tools.add_entry_to_config(
                    self.master.user_data_path,
                    'Meter',
                    'night_meter',
                    self.master.credentials_frame.entry_nightmeter.get())
                self.master.logger.info('New night meter number added to config')



            # Make credentials available in user instance
            self.master.user.Login['username'] = self.master.credentials_frame.entry_username.get()
            self.master.user.Login['password'] = pwd_str
            self.master.user.Meter['day_meter'] = self.master.credentials_frame.entry_daymeter.get()
            self.master.user.Meter['night_meter'] = self.master.credentials_frame.entry_nightmeter.get()
            self.master.logger.debug('Save credentials routine triggered')

        else:
            # Temporary store credentials in user instance
            self.master.user.Login['username'] = self.master.credentials_frame.entry_username.get()
            self.master.user.Login['password'] = pwd_str
            self.master.user.Meter['day_meter'] = self.master.credentials_frame.entry_daymeter.get()
            self.master.user.Meter['night_meter'] = self.master.credentials_frame.entry_nightmeter.get()
            self.master.logger.debug('Credentials temporarily added to user attributes')

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