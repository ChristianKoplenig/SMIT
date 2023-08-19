"""
Tools for handling the password input/save dialog
"""
import tkinter as tk
from tkinter import ttk
from modules.user import user
from modules.rsahandling import RsaTools

class UiTools():
    """Password input and save dialog
    """
    def __init__(self, user) -> None:
        
        self.user = user
        
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
        else:
            print('unchecked')
            self.user.password = self.pwd_entry.get()
            print(self.user.password)
            
        va1 = self.pwd_entry.get()
        print(va1)
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