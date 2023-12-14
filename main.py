"""Main entry point for SMIT
"""
from smit.application import Application
from gui.main_window import AppGui

class SMIT:
    """Main entry point
    """
    def __init__(self) -> None:
        self.user = Application()
        self.root = AppGui(self.user)
        self.root.mainloop()

        if self.user.dummy is True:
            self.dummy_reload()



    def dummy_reload(self) -> None:
        """Reload the root window with dummy settings.
        """
        self.user.logger.info(' ---- Reload with dummy configuration ---- ')
        self.user = Application(True)
        self.root = AppGui(self.user)
        self.root.mainloop()

SMIT()
