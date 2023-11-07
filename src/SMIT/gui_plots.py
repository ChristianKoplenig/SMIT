"""Helper class for buttons frame in ctk GUI

---
'Classes for frames to build main GUI interface
-----------------------------------------------

    - Helper classes for GUI

Typical usage:
    Call class in AppGui
"""
import customtkinter as ctk
import matplotlib
from matplotlib import figure

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

# # Plot
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.gridspec as gridspec

class PlotFrame(ctk.CTkFrame):
    """Frame for plots

    - year overview
    - month overview
    - week with folling mean

    Args:
        ctk (_type_): _description_
    """
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.df_day = self._create_dataframes('day_meter')
        self.df_night = self._create_dataframes('night_meter')

        # maybe put this into one frame to use navigation toolbar
        day = self._seaborn_bar_plot(self.df_day, 'Day').get_tk_widget()
        day.grid(row=0, pady=20)

        night = self._seaborn_bar_plot(self.df_night, 'Night').get_tk_widget()
        night.grid(row=1)

    def _create_dataframes(self, meter):
        """Generate data frames for plots
        args: meter --> 'day_meter';'night_meter'
        """
        dataframe = self.master.user.os_tools.create_dataframe(
            self.master.user.Folder['work_daysum'], 
            self.master.user.Meter[meter])
        return dataframe
           
    def _mpl_bar_plot(self,df,title) -> FigureCanvasTkAgg:
        """Draw a matplotlib bar chart
        """

        # create a figure
        figure = Figure(figsize=(9, 3), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)

        # create the toolbar
        #NavigationToolbar2Tk(figure_canvas, self)

        # create axes
        axes = figure.add_subplot()

        # create the barchart
        axes.bar(df['date'], df['verbrauch'])
        axes.set_title(title)
        axes.set_ylabel('Wh')
        return figure_canvas

    def _seaborn_bar_plot(self, df, title):
        """Plot data with seaborn module
        """
        figure = Figure(figsize =(9,3), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self)

        axes = figure.add_subplot()

        sns.barplot(data=df,
                    x='date',
                    y='verbrauch',
                    ax=axes)
        
        axes.set_ylabel('Verbrauch [Wh]', labelpad = 0, fontsize = 12)
        axes.xaxis.set_major_locator(md.MonthLocator())
        axes.xaxis.set_major_formatter(md.DateFormatter('%b'))
        axes.set_title(title)
        axes.set_xlabel('')
        return figure_canvas