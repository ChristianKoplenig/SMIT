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
import pandas as pd
import datetime as dt

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

# # Plot
import seaborn as sns
import matplotlib.dates as md

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

        # Create dataframes
        self.slice_start = str((dt.datetime.today() - dt.timedelta(days=8)))[:10]
        self.slice_end = str((dt.datetime.today() - dt.timedelta(days=1)))[:10]
        self.df_day = self._create_dataframes('day_meter')
        self.df_night = self._create_dataframes('night_meter')
        self.df_slice = self._slice_dataframe(self.slice_start, self.slice_end, 'day_meter')

        # maybe put this into one frame to use navigation toolbar
        day = self._seaborn_bar_plot(self.df_day, 'Day').get_tk_widget()
        day.grid(row=0)

        night = self._seaborn_bar_plot(self.df_night, 'Night').get_tk_widget()
        night.grid(row=1)

        day_slice = self._seaborn_slice_plot(self.df_slice, 'Last Week').get_tk_widget()
        day_slice.grid(row=2)

    def _create_dataframes(self, meter) -> pd.DataFrame:
        """Generate data frames for plots
        args: meter --> 'day_meter';'night_meter'
        """
        dataframe = self.master.user.os_tools.create_dataframe(
            self.master.user.Folder['work_daysum'], 
            self.master.user.Meter[meter])
        return dataframe
    
    def _slice_dataframe(self, st_date: str, end_date: str, metertype: str) -> pd.DataFrame:
        """Create sliced dataframe for plots

        """
        dataframe = self.master.user.os_tools.slice_dataframe(
            st_date,
            end_date,
            self.master.user.Folder['work_daysum'], 
            self.master.user.Meter[metertype]
        )
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

        # Format xlabel
        myFmt = md.DateFormatter('%Y')
        axes.xaxis.set_major_formatter(myFmt)

        return figure_canvas

    def _seaborn_bar_plot(self, df, title) -> FigureCanvasTkAgg:
        """Plot data with seaborn module
        """
        figure = Figure(figsize =(9,3), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self)

        axes = figure.add_subplot()

        sns.barplot(data=df,
                    x='date',
                    y='verbrauch',
                    color='#3a7ebf',
                    ax=axes)
        
        axes.set_ylabel('Verbrauch [Wh]', labelpad = 0, fontsize = 12)
        axes.xaxis.set_major_locator(md.MonthLocator())
        axes.xaxis.set_major_formatter(md.DateFormatter('%b'))

        axes.set_title(title)
        axes.set_xlabel('')
        return figure_canvas
    
    def _seaborn_slice_plot(self, df, title) -> FigureCanvasTkAgg:
        """Plot data with seaborn module
        """
        figure = Figure(figsize =(9,3), dpi=100)


        figure_canvas = FigureCanvasTkAgg(figure, self)


        axes = figure.add_subplot()

        sns.barplot(data=df,
                    x='date',
                    y='verbrauch',
                    color='#3a7ebf',
                    ax=axes)
        
        axes.set_ylabel('Verbrauch [Wh]', labelpad = 0, fontsize = 12)

        # Define date element
        x_dates = df['date'].dt.date
        # Define formatting for x labels
        x_date = x_dates.apply(lambda x: x.strftime('%a'))

        axes.set_xticklabels(labels=x_date)
        axes.set_title(title)
        axes.set_xlabel('')

        return figure_canvas