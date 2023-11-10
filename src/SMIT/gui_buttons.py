"""Helper class for buttons frame in ctk GUI

---
'Classes for frames to build main GUI interface
-----------------------------------------------

    - Helper classes for GUI

Typical usage:
    Call class in AppGui
"""
import customtkinter as ctk
import base64

class ButtonFrame(ctk.CTkFrame):
    """Frame for buttons

    Args:
        ctk (_type_): _description_

    Returns:
        _type_: _description_
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

    def _button_update_data(self) -> None:
        """trigger scrape move routine
        """
        self.master.user.os_tools.sng_scrape_and_move()
        self.master.reload_plots()

    def _button_close(self) -> None:
        """Event on close button press
        """
        print('All tk windows closed on button press')
        self.quit()

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
            
    def _button_savecred(self) -> None:
        """Define accept button action.

        If the "Save user credentials..." checkbox is activated then the 
        entered data will be added to the `user_data.toml` file 
        and the user instance.  
        Else everything entered will be added to the active user instance and
        won't get stored in a file.
        """
        ################### debug
        print('btn save cred pressed')

        #Encrypt credentials with rsa keys
        pwd_enc = self.master.user.rsa.encrypt_pwd(
            self.master.credentials_frame.entry_password.get())
        # Convert password to str representation for storing it in `user_data.toml`
        pwd_str = base64.b64encode(pwd_enc).decode('utf-8')

        save_credentials_activated = self.master.checkbox_frame.save_credentials.get()

        #if self.master.checkbox_frame.save_credentials.get() == 'on':
        if save_credentials_activated:

            #############debug
            print('checkbox check succed')


            # Append credentials to user_data.toml
            if pwd_str == self.master.credentials_frame.entry_password.get():
                print('password not changed')
            else:
                self.master.user.toml_tools.add_entry_to_config(
                    self.master.user_data_path,
                    'Login',
                    'password',
                    pwd_str)
            
            if self.master.user.Login['username'] == self.master.credentials_frame.entry_username.get():
                print('user not changed')
            else:
                self.master.user.toml_tools.add_entry_to_config(
                    self.master.user_data_path,
                    'Login',
                    'username',
                    self.master.credentials_frame.entry_username.get())
                
            if self.master.user.Meter['day_meter'] == self.master.credentials_frame.entry_daymeter.get():
                print('daymeter not changed')
            else:            
                self.master.user.toml_tools.add_entry_to_config(
                    self.master.user_data_path,
                    'Meter',
                    'day_meter',
                    self.master.credentials_frame.entry_daymeter.get())

            if self.master.user.Meter['night_meter'] == self.master.credentials_frame.entry_nightmeter.get():
                print('nightmeter not changed')
            else:            
                self.master.user.toml_tools.add_entry_to_config(
                    self.master.user_data_path,
                    'Meter',
                    'night_meter',
                    self.master.credentials_frame.entry_nightmeter.get())



            # Make credentials available in user instance
            self.master.user.Login['username'] = self.master.credentials_frame.entry_username.get()
            self.master.user.Login['password'] = pwd_str
            self.master.user.Meter['day_meter'] = self.master.credentials_frame.entry_daymeter.get()
            self.master.user.Meter['night_meter'] = self.master.credentials_frame.entry_nightmeter.get()
            self.master.logger.debug('Credentials permanently added to user data')

        else:
            # Temporary store credentials in user instance
            self.master.user.Login['username'] = self.master.credentials_frame.entry_username.get()
            self.master.user.Login['password'] = pwd_str
            self.master.user.Meter['day_meter'] = self.master.credentials_frame.entry_daymeter.get()
            self.master.user.Meter['night_meter'] = self.master.credentials_frame.entry_nightmeter.get()
            self.master.logger.debug('Credentials temporarily added to user attributes')