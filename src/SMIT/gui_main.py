"""GUI

---
'Custom TKinter Framework`
-------------------------

- Main entry point for the application.

Typical usage:
    On startup
"""
import customtkinter as ctk
import pathlib as pl

from SMIT.gui_credentials import CredentialsFrame
from SMIT.gui_buttons import ButtonFrame
from SMIT.gui_checkboxes import CheckboxFrame
from SMIT.gui_plots import PlotFrame
from SMIT.gui_stats import StatsFrame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from SMIT.application import Application

### Developement imports
from SMIT.application import Application

class AppGui(ctk.CTk):
    """Main GUI class

    ---

    Use as entry point.
    Generate main application window.

    Args:
        ctk (_type_): _description_
    """
    
    def __init__(self, app: 'Application') -> None:
        super().__init__()

        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("light")

        self.user = app
        self.user_data_path = pl.Path(self.user.Path['user_data'])

        if self.user.dummy is True:
            ctk.set_appearance_mode('dark')

        # Logger setup
        self.logger = app.logger
        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)

        # Main window
        self.title("SMIT")
        self.geometry("1440x900")
        self.grid_columnconfigure((0, 1), weight=1)

        # Frames
        self.credentials_frame = CredentialsFrame(self)
        self.credentials_frame.grid(row=0, column=0, sticky='ew')

        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=1,column=0, sticky='ew')
        
        self.checkbox_frame = CheckboxFrame(self)
        self.checkbox_frame.grid(row=2, column=0, sticky='ew')

        self.plot_frame = PlotFrame(self)
        self.plot_frame.grid(row=0, column=1, rowspan=4, sticky='ew')
        
        self.stats_frame = StatsFrame(self)
        self.stats_frame.grid(row=3, column=0, sticky='ew')


    def reload_plots(self) -> None:
        """Desroy and re-init the plot frame
        """
        #Debug
        print('---------------------')
        print('update button pressed') 
        self.plot_frame.destroy()
        self.plot_frame = PlotFrame(self)
        self.plot_frame.grid(row=0, column=1, rowspan=4, sticky='ew')
        #self.master.root.update()

    def initiate_dummy(self) -> None:
        """Set dummy flag and close root window.
        """
        self.user.dummy = True
        self.destroy()

    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"
    
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