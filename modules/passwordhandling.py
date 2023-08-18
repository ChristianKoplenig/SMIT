"""
Tools for handling the password input/save dialog
"""
import tkinter as tk
from tkinter import ttk

class UiTools():
    """Password input and save dialog
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title('Enter Password')
        self.root.geometry('300x200')
        self.checkbox_value = tk.StringVar()
        #self.root.mainloop()

    def checkbox_changed(self):
        """Do something when the checkbox is checked.
        """
        ch =  self.checkbox_value.get()
        print(ch)
    
    def pwd_dialog(self):
        ttk.Checkbutton(self.root,
                        text= 'save password',
                        command= self.checkbox_changed,
                        onvalue='yes',
                        offvalue='no',
                        variable= self.checkbox_value).pack()
        self.root.mainloop()
    
    
UiTools().pwd_dialog()