"""GUI

---
'Custom TKinter Framework`
-------------------------

- Main entry point for the application.

Typical usage:
    On startup
"""
import customtkinter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from SMIT.application import Application

class AppGui(customtkinter.CTk):
    """Main GUI class

    ---

    Use as entry point.
    Generate main application window.

    Args:
        customtkinter (_type_): _description_
    """
    def __init__(self):
        super().__init__()

        self.title("SMIT")
        self.geometry("1440x900")

app = AppGui()
app.mainloop()

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