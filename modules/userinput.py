"""
Tools for handling the password input/storing dialog
"""
import tkinter as tk
from tkinter import ttk
import pathlib as pl
import base64
# Custom Modules
from modules.filehandling import TomlTools
from modules.rsahandling import RsaTools

class UiTools():
    """Tools for interacting with the tkinter library.
    
    Attributes:
    -----------
    user : class instance
        Hold user information
        
    Methods
    -------
    tk_text(txt_input):
        Generates text widget
    tk_checkbox():
        Generates the save password checkbox.
    button_action():
        Reads input from entry field, handles pwd routine.
    password_dialog():
        Routine for getting the user input
    """
    def __init__(self, user: 'user') -> None:
        """Initialize Class with all attributes from `UserClass`

        Parameters
        ----------
        user : class instance
            User data initiated via `user()` function from user module            
        """                
        self.user = user
        
        self.user_data = pl.Path(self.user.Path['user_data'])
        
        self.window = tk.Tk()
        self.window.title('Password Dialog')
        self.window.geometry('400x200')
        
        self.pwd_entry = tk.StringVar()
        self.checkbox_value = tk.BooleanVar(False)
        
        self.button = tk.Button(
            text = 'Confirm',
            command= self.button_action
        )
        
        self.entry = tk.Entry(
            fg='yellow',
            bg='blue',
            textvariable= self.pwd_entry,
            show= '*'
        )
        
    def tk_text(self, txt_input: str) -> None:
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
        
    def tk_checkbox(self) -> None:
        """Generate checkbox for password saving option.
        """
        ttk.Checkbutton(
            self.window,
            text= 'Save encrypted password in user_data',
            variable= self.checkbox_value
        ).pack()
        
    def button_action(self) -> None:
        """Defines what to todo when accept button is pressed.
        
        If the "save password" checkbox is activated then the password
        will be added to the `user_data.toml` file and the user instance.
        Else the password will be added just to the user instance.
        """
        #Encrypt password with rsa keys
        pwd_enc = RsaTools(self.user).encrypt_pwd(self.pwd_entry.get())
        # Convert password to str representation for storing it in `user_data.toml`
        pwd_str = base64.b64encode(pwd_enc).decode('utf-8')
        
        user_data_path = pl.Path(self.user.Path['user_data'])
        save_pwd_activated = self.checkbox_value.get()
        
        if save_pwd_activated:

            # Append password to user_data.toml
            TomlTools(self.user).toml_save_password(user_data_path, pwd_str)
            # Make password available in user instance
            self.user.Login['password'] = pwd_str
        
        else:
            # Temporary store password in user instance 
            self.user.Login['password'] = pwd_str
            
        self.window.destroy()
        
    def password_dialog(self) -> None:
        """Initiate "Enter Password" GUI
        """
        self.tk_text('Please enter your Stromnetz Graz password')
        self.entry.pack()
        self.entry.focus()
        self.tk_checkbox()
        self.button.pack()
        self.tk_text('Please read the disclaimer for details on password handling')
        self.window.mainloop()