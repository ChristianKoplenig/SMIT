"""Helper class for checkboxes frame in CustomTkinter GUI

---
'Classes for frames to build main GUI interface
-----------------------------------------------

    - Helper classes for GUI

Typical usage:
    Call class in AppGui
"""
import customtkinter as ctk

class CheckboxFrame(ctk.CTkFrame):
    """Generate checkboxes in top row

    Args:
        ctk (customtkinter): Inherit from frame class
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
            command=self._save_credentials,
            variable=self.save_credentials,
            onvalue=True,
            offvalue=False
        )
        self.save_credentials_chkbx.grid(row=1, padx=10)




    def _save_credentials(self) -> None:
        """Helper function for credentials checkbox
        """    
        print('cred chkbx: ',self.save_credentials.get())