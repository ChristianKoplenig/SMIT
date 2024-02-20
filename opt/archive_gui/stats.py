"""Create variables tabel.

---

- Draw a widget for single data variables

Typical usage:

    windowframe = StatsFrame()
"""
import tkinter as tk
import customtkinter as ctk

class StatsFrame(ctk.CTkFrame):
    """Generate frame with statistic data

    - Create label widgets
    - Create entry widgets
    - Show rolling median value for:   
        - last seven days
        - last 30 days

    Returns:

    """
    def __init__(self, master):
        super().__init__(master)

        # Text variables for entries
        self.stat_week = tk.StringVar(value=master.plot_frame.df_slice.iloc[-1,-1])
        self.stat_month = tk.StringVar(value=master.plot_frame.df_slice.iloc[-1,-2])


        self.title = ctk.CTkLabel(
            self,
            text='Stats')
        self.title.grid(row=0, padx=10, pady=(0,20), sticky='ew', columnspan=2)

        self.week_lbl = ctk.CTkLabel(
            self,
            text='Last week [Wh/day]: '
        )
        self.week_lbl.grid(row=1, column=0, padx=20, pady=5)
        self.month_lbl = ctk.CTkLabel(
            self,
            text='Last month [Wh/day]: '
        )
        self.month_lbl.grid(row=2, column=0, padx=20, pady=5)

        # Entries
        self.entry_week = ctk.CTkEntry(
            self,
            textvariable=self.stat_week,
            width=75)
        self.entry_week.grid(row=1, column=1, padx=(20, 20), pady=5)

        self.entry_month = ctk.CTkEntry(
            self,
            textvariable=self.stat_month,
            width=75)
        self.entry_month.grid(row=2, column=1, padx=(20, 20), pady=5)

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