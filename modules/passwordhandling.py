"""
Tools for handling the password input/save dialog
"""
import tkinter as tk
from tkinter import ttk

class UiTools():
    """Password input and save dialog
    """

    def __init__(self) -> None:
        
        # create window
        self.window = tk.Tk()
        self.window.title('Password Dialog')
        self.window.geometry('300x200')
        
        self.checkbox_value = tk.StringVar()
    
    def tk_text(self, txt_input):
        """Generate text widget
        """
        text = tk.Label(
            text= txt_input,
            height=3)
        text.pack()
        
    def tk_button(self):
        """Generate button
        """
        button = tk.Button(
            text='Confirm'
        )
        button.pack()    

    def tk_checkbox(self):
        """Do something when the checkbox is checked.
        """
        ch =  self.checkbox_value.get()
        print(ch)
        
    def tk_entry(self):
        """Generate text entry field for password input.
        """
        entry = tk.Entry(
            fg='yellow',
            bg='blue',
            width=15
        )
        entry.pack()
    
    def pwd_dialog(self):
        """Initiate enter password dialog
        """
        self.tk_text('Please enter Password')
        #self.tk_entry()
        pwd = tk.Entry(fg='yellow', bg='blue', width=15)
        pwd.pack()
        print(pwd.get())
        ttk.Checkbutton(self.window,
                        text= 'save password',
                        command= self.tk_checkbox,
                        onvalue='yes',
                        offvalue='no',
                        variable= self.checkbox_value).pack()
        self.tk_button()
        self.tk_text('See disclaimer for information on password storage')
        self.window.mainloop()
    
    
UiTools().pwd_dialog()