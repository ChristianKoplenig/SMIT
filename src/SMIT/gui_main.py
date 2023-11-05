"""GUI

---
'Custom TKinter Framework`
-------------------------

- Main entry point for the application.

Typical usage:
    On startup
"""
import customtkinter
import pathlib as pl

from SMIT.gui_credentials import CredentialsFrame
from SMIT.gui_buttons import ButtonFrame
from SMIT.gui_checkboxes import CheckboxFrame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from SMIT.application import Application

### Developement imports
from SMIT.application import Application

class AppGui(customtkinter.CTk):
    """Main GUI class

    ---

    Use as entry point.
    Generate main application window.

    Args:
        customtkinter (_type_): _description_
    """


    def __init__(self, app: 'Application') -> None:
        super().__init__()

        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("dark")

        self.user = app
        self.user_data_path = pl.Path(self.user.Path['user_data'])

        self.close_callback = False

        # Logger setup
        self.logger = app.logger
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)

        # Main window
        self.title("SMIT")
        self.geometry("1440x900")
        self.grid_columnconfigure(0, weight=1)
        #self.grid_rowconfigure(0, weight=1)

        # Frames
        self.credentials_frame = CredentialsFrame(self)
        self.credentials_frame.grid(row=0, column=0, sticky='w')

        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=0,column=1)
        
        self.checkbox_frame = CheckboxFrame(self)
        self.checkbox_frame.grid(row=0, column=2)





    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"
    

user = Application()
ctk = AppGui(user)
ctk.mainloop()


















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