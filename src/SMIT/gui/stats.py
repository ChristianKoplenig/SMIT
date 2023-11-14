"""Helper class for stats frame in CustomTkinter GUI

---
'Classes for frames to build main GUI interface
-----------------------------------------------

    - Helper classes for GUI

Typical usage:
    Call class in AppGui
"""
import tkinter as tk
import customtkinter as ctk
import pandas

class StatsFrame(ctk.CTkFrame):
    """Generate frame with statistics

    Args:
        ctk (customtkinter): Inherit from frame class
    """
    def __init__(self, master):
        super().__init__(master)

        #self.master = master

        # Text variables for entries
        self.stat_week = tk.StringVar(value=master.plot_frame.df_day.iloc[-1,4])
        self.stat_month = tk.StringVar(value=master.plot_frame.df_day.iloc[-1,3])


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


        # entries
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