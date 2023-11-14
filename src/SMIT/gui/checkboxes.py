"""Save credentials checkbox.

---

- Checkbox for saving user credentials

Typical usage:

    windowframe = CheckboxFrame()
"""
import customtkinter as ctk

class CheckboxFrame(ctk.CTkFrame):
    """Generate frame with checkbox.

    Attributes:

        `ctk.CTkFrame`  

    Returns:

    """
    def __init__(self, master):
        super().__init__(master)

        self.title = ctk.CTkLabel(
            self,
            text='Options')
        self.title.grid(row=0, padx=10, pady=(50,20), sticky='ew')

        self.save_credentials = ctk.BooleanVar(value=False)
        self.save_credentials_chkbx = ctk.CTkCheckBox(
            self,
            text='Save credentials',
            variable=self.save_credentials,
            onvalue=True,
            offvalue=False
        )
        self.save_credentials_chkbx.grid(row=1, padx=10)

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