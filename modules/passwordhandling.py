"""
Tools for handling the password input/save dialog
"""
import sys
import tkinter as tk
from tkinter import ttk
import pathlib as pl
#from modules.user import user
if sys.version_info < (3, 11):
    import tomli as tomlib
else:
    import tomlib
from modules.rsahandling import RsaTools

class UiTools():
    """Password input and save dialog
    """
    def __init__(self, user) -> None:
        
        self.user = user
        
        self.user_data = pl.Path(self.user.user_data_path)
        
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
        
    def tk_text(self, txt_input):
        text = tk.Label(
            text= txt_input,
            height=3
        )
        text.pack()
        
    def tk_checkbox(self):
        ttk.Checkbutton(
            self.window,
            text= 'save pwd',
            #state= 0,
            #command= self.checkbox_action,
            #onvalue= 1,
            #offvalue= 0,
            variable= self.checkbox_value
        ).pack()
        
    # def checkbox_action(self):
    #     val = self.checkbox_value.get()
    #     print(val)
        
    def button_action(self):
        
        if self.checkbox_value.get():
            print('checked')
            print(self.user.username)
            
            with open(self.user_data, 'wb') as file:
                data = tomlib.load(file)
                data['pwd'] = 'test.pwd'
                
                #for key, value in data.items():
                #     setattr(self, 'pass', 'word')
                    #data['pwd'] = 'test.pwd'
                #setattr(self, 'password', 'test')
        
        else:
            print('unchecked')
            self.user.password = RsaTools(self.user).encrypt_pwd(self.pwd_entry.get())
            print(self.user.password)
            
            
        self.window.destroy()
        
    def pwd_dialog(self):
        self.tk_text('Please enter your Stromnetz Graz password')
        self.entry.pack()
        self.entry.focus()
        self.tk_checkbox()
        self.button.pack()
        self.tk_text('Please read the disclaimer for details on password handling')
        self.window.mainloop()
    
    
#UiTools().pwd_dialog()