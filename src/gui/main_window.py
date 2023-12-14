"""Arrange main window.

----

- Logger setup
- Theme
- Main window grid and properties

Typical usage:

    user = Application()
    window = AppGui(user)
"""
import pathlib as pl
import customtkinter as ctk

from smit.application import Application

from gui.credentials import CredentialsFrame
from gui.buttons import ButtonFrame
from gui.checkboxes import CheckboxFrame
from gui.plots import PlotFrame
from gui.stats import StatsFrame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smit.application import Application

class AppGui(ctk.CTk):
    """Build main window for SMIT Gui.

    - Root window setup
    - Load dummy theme
    - Logger
    - Reload plot frame
    - Window restart for dummy usage

    Attributes:
        app (Application): Userdata and config information.
    """
    
    def __init__(self, app: 'Application') -> None:
        super().__init__()

        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("light")

        self.user = app
        self.user_data_path = pl.Path(self.user.Path['user_data'])
        self.wdempty = pl.Path(self.user.Folder['work_daysum'])


        if self.user.dummy is True:
            ctk.set_appearance_mode('dark')
            self.user.os_tools._move_files_to_workdir('199996')
            self.user.os_tools._move_files_to_workdir('199997')

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
        
        if not any(self.wdempty.iterdir()):
            
            self.logger.info('Raw input folder empty. Update data')
        else:

            self.plot_frame = PlotFrame(self)
            self.plot_frame.grid(row=0, column=1, rowspan=4, sticky='ew')

            self.stats_frame = StatsFrame(self)
            self.stats_frame.grid(row=3, column=0, sticky='ew')

        self.logger.info(f'Gui root window with dummy: {self.user.dummy} loaded')

    def reload_plots(self) -> None:
        """Call `PlotFrame` class.
        """
        if hasattr(self, 'plot_frame'):
            self.plot_frame.destroy()

        if hasattr(self, 'stats_frame'):
            self.stats_frame.destroy()

        self.plot_frame = PlotFrame(self)
        self.plot_frame.grid(row=0, column=1, rowspan=4, sticky='ew')

        self.stats_frame = StatsFrame(self)
        self.stats_frame.grid(row=3, column=0, sticky='ew')
        
        self.logger.debug('Plots/Stats frame reloaded')

    def initiate_dummy(self) -> None:
        """Set dummy flag and close main window.
        """
        self.user.dummy = True
        self.destroy()

        self.logger.debug('Destroy root window for dummy restart')

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