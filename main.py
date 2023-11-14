"""Main entry point for SMIT
"""
from SMIT.application import Application
from SMIT.gui.main_window import AppGui

class SMIT:
    """Main entry point
    """
    def __init__(self) -> None:
        self.user = Application()
        self.root = AppGui(self.user)
        self.root.mainloop()

        if self.user.dummy is True:
            print('dummy true main detected')
            self.rw_reload()



    def rw_reload(self) -> None:
        """Reload the root window with dummy settings.
        """
        self.user = Application(True)
        self.root = AppGui(self.user)
        self.root.mainloop()

SMIT()
