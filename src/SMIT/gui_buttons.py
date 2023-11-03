"""Helper class for buttons frame in CustomTkinter GUI

---
'Classes for frames to build main GUI interface
-----------------------------------------------

    - Helper classes for GUI

Typical usage:
    Call class in AppGui
"""
import customtkinter
import base64

class ButtonFrame(customtkinter.CTkFrame):
    """Frame for buttons

    Args:
        customtkinter (_type_): _description_

    Returns:
        _type_: _description_
    """
    def __init__(self, master):
        super().__init__(master)

        #Button list
        # - confirm

        self.master = master
    
        self.button_close = customtkinter.CTkButton(
            master=self,
            text='Close Application',
            command=self._button_close
        )
        self.button_close.grid(row=0)

        self.button_delpwd = customtkinter.CTkButton(
            master=self,
            text='Delete Password',
            command=self._button_delpwd
        )
        self.button_delpwd.grid(row=1)

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
            
    # def _button_accept(self) -> None:
    #     """Define accept button action.

    #     If the "Save user credentials..." checkbox is activated then the 
    #     entered data will be added to the `user_data.toml` file 
    #     and the user instance.  
    #     Else everything entered will be added to the active user instance and
    #     won't get stored in a file.
    #     """
    #     # Encrypt credentials with rsa keys
    #     pwd_enc = self.master.user.rsa.encrypt_pwd(
    #         self.master.credentials_frame.password.get())
    #     # Convert password to str representation for storing it in `user_data.toml`
    #     pwd_str = base64.b64encode(pwd_enc).decode('utf-8')

    #     #save_credentials_activated = self.save_credentials.get()

    #     if save_credentials_activated:

    #         # Append credentials to user_data.toml
    #         self.master.user.toml_tools.add_entry_to_config(
    #             self.master.user_data_path,
    #             'Login',
    #             'password',
    #             pwd_str)
    #         self.master.user.toml_tools.add_entry_to_config(
    #             self.master.user_data_path,
    #             'Login',
    #             'username',
    #             self.master.entry_username.get())
    #         self.master.user.toml_tools.add_entry_to_config(
    #             self.master.user_data_path,
    #             'Meter',
    #             'day_meter',
    #             self.master.entry_meter_day.get())
    #         self.master.user.toml_tools.add_entry_to_config(
    #             self.master.user_data_path,
    #             'Meter',
    #             'night_meter',
    #             self.master.entry_meter_night.get())
    #         # Make credentials available in user instance
    #         self.master.user.Login['username'] = self.entry_username.get()
    #         self.master.user.Login['password'] = pwd_str
    #         self.master.user.Meter['day_meter'] = self.entry_meter_day.get()
    #         self.master.user.Meter['night_meter'] = self.entry_meter_night.get()
    #         self.master.logger.debug('Credentials permanently added to user data')

    #     else:
    #         # Temporary store credentials in user instance
    #         self.master.user.Login['username'] = self.entry_username.get()
    #         self.master.user.Login['password'] = pwd_str
    #         self.master.user.Meter['day_meter'] = self.entry_meter_day.get()
    #         self.master.user.Meter['night_meter'] = self.entry_meter_night.get()
    #         self.master.logger.debug('Credentials temporarily added to user attributes')