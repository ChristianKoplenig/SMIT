import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title('Enter Password')
root.geometry('300x200')

checkbox_value = tk.StringVar()

def checkbox_changed():
    """Do something when the checkbox is checked.
    """
    ch =  checkbox_value.get()
    print(ch)

ttk.Checkbutton(root,
                text= 'save password',
                command= checkbox_changed,
                onvalue='yes',
                offvalue='no',
                variable= checkbox_value).pack()

root.mainloop()