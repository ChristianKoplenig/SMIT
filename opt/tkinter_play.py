import tkinter as tk
from tkinter import ttk

class TkPlay():
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title('Password Dialog')
        self.window.geometry('300x200')
        
        self.pwd_entry = tk.StringVar()
        self.checkbox_value = tk.StringVar()
        
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
            command= self.checkbox_action,
            onvalue= 'checked',
            offvalue= 'unchecked',
            variable= self.checkbox_value
        ).pack()
        
    def checkbox_action(self):
        val = self.checkbox_value.get()
        print(val)
        
    def button_action(self):
        val = self.pwd_entry.get()
        print(val)
        
    def pwd_dialog(self):
        self.tk_text('enter pwd')
        self.entry.pack()
        self.entry.focus()
        self.tk_checkbox()
        self.button.pack()
        self.tk_text('disclaimer')
        self.window.mainloop()

TkPlay().pwd_dialog()        