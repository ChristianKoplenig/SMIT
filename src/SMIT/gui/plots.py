"""Create dataframes, draw plots.

---

- Create pandas dataframes
- Use matplotlib and seaborn to draw plots 

Typical usage:

    windowframe = PlotFrame()
"""
import datetime as dt
import pandas as pd
import matplotlib
import matplotlib.dates as md
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import seaborn as sns
import customtkinter as ctk

matplotlib.use('TkAgg')

class PlotFrame(ctk.CTkFrame):
    """Setup plot column for SMIT Gui.

    - Define slice dates
    - Create day/night/slice dataframe
    - Create and arrange widgets for matplotlib canvases
    - Functions to draw matplotlib canvases

    Returns:

    """
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        if self.master.user.dummy is True:
            self.slice_start = '2023-03-24'
            self.slice_end = '2023-03-31'
        else:          
            self.slice_start = str((dt.datetime.today() - dt.timedelta(days=7)))[:10]
            self.slice_end = str((dt.datetime.today() - dt.timedelta(days=1)))[:10]
        
        # Create dataframes
        self.df_day = self._create_dataframes('day_meter')
        self.df_night = self._create_dataframes('night_meter')
        self.df_slice = self._slice_dataframe(self.slice_start, self.slice_end, self.df_day, self.df_night)

        # Create plots
        day = self._seaborn_bar_plot(self.df_day, 'Day').get_tk_widget()
        day.grid(row=0)

        night = self._seaborn_bar_plot(self.df_night, 'Night').get_tk_widget()
        night.grid(row=1)

        day_slice = self._mpl_slice_plot(self.df_slice, 'Last Week').get_tk_widget()
        day_slice.grid(row=2)

    def _create_dataframes(self, meter: str) -> pd.DataFrame:
        """Generate data frames for plots.
        
        Attributes:

            meter (str): Meter number to identify raw `.csv` files  

        Returns:
            dataframe (`pd.DataFrame`): Power readings for given meter
        """
        dataframe = self.master.user.os_tools.create_dataframe(
            self.master.user.Folder['work_daysum'], 
            self.master.user.Meter[meter])
        
        return dataframe
    
    def _slice_dataframe(self, st_date: str, end_date: str, day: pd.DataFrame, night: pd.DataFrame) -> pd.DataFrame:
        """Create sliced dataframe for plots.

        Attributes:

            st_date (str): Start date for data slice; Format: 'YYYY-MM-DD'  
            end_date (str): End date for data slice; Format: 'YYYY-MM-DD' 
            day (pd.DataFrame): Data frame with measurements for day meter 
            night (pd.DataFrame): Data frame with measurements for night meter 

        Returns:
            dataframe (`pd.DataFrame`): Sum of power readings for day/night meter

        """
        df_day = day[['date', 'verbrauch']]
        df_night = night[['date', 'verbrauch']]
        
        df_sum = pd.merge(df_day, df_night, on='date', suffixes=('_day', '_night'))
        df_sum['sum_verbrauch'] = df_sum['verbrauch_day'] + df_sum['verbrauch_night']
        df_sum = df_sum.round(0)

        df_sum['median30'] = df_sum['sum_verbrauch'].rolling(30).median()
        df_sum['median7'] = df_sum['sum_verbrauch'].rolling(7).median()

        dataframe = df_sum[['date', 'sum_verbrauch', 'median30', 'median7']]
        dataframe = dataframe[(dataframe['date'] >= st_date) & (dataframe['date'] <= end_date)]

        self.master.logger.debug(f'Sliced dataframe with start: {st_date} and end: {end_date} created')

        return dataframe
          
    def _mpl_bar_plot(self,df: pd.DataFrame,title: str) -> FigureCanvasTkAgg:
        """Draw a matplotlib bar plot.

        Args:
            df (pd.DataFrame): Input data for plot
            title (str): Title for plot

        Returns:
            FigureCanvasTkAgg: Input canvas for gui widget
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

        # Format labels
        axes.xaxis.set_major_locator(md.MonthLocator())
        axes.xaxis.set_major_formatter(md.DateFormatter('%b'))
        axes.set_ylabel('Consumption [Wh]', labelpad = 0, fontsize = 12)

        axes.set_title(title)
        #axes.set_xlabel('')

        return figure_canvas

    def _seaborn_bar_plot(self, df, title) -> FigureCanvasTkAgg:
        """Draw a seaborn bar plot on a matplotlib canvas.

        Args:
            df (pd.DataFrame): Input data for plot
            title (str): Title for plot

        Returns:
            FigureCanvasTkAgg: Input canvas for gui widget
        """
        figure = Figure(figsize =(9,3), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self)

        axes = figure.add_subplot()

        sns.barplot(data=df,
                    x='date',
                    y='verbrauch',
                    color='#3a7ebf',
                    ax=axes)
        
        axes.set_ylabel('Consumption [Wh]', labelpad = 0, fontsize = 12)
        axes.xaxis.set_major_locator(md.MonthLocator())
        axes.xaxis.set_major_formatter(md.DateFormatter('%b'))

        axes.set_title(title)
        axes.set_xlabel('')
        return figure_canvas
    
    def _mpl_slice_plot(self, df, title) -> FigureCanvasTkAgg:
        """Use sliced dataframe for matplotlib bar plot.

        Args:
            df (pd.DataFrame): Input data for plot
            title (str): Title for plot

        Returns:
            FigureCanvasTkAgg: Input canvas for gui widget
        """
        figure = Figure(figsize =(9,3), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self)
        
        axes = figure.add_subplot()
        axes.bar(df['date'], df['sum_verbrauch'])

        myFmt = md.DateFormatter('%a')
        axes.xaxis.set_major_formatter(myFmt)

        axes.set_title(title)
        axes.set_xlabel('')
        axes.spines[['top', 'bottom', 'right', 'left']].set_visible(False)
        axes.set_ylabel('Consumption [Wh]', labelpad = 0, fontsize = 12)
        axes.bar_label(axes.containers[0])  # show values with bars

        return figure_canvas
    
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