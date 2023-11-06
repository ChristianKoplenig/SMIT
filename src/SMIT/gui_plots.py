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

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

# # Plot
# import seaborn as sns
# import matplotlib.pyplot as plt
# import matplotlib.dates as md
# import matplotlib.gridspec as gridspec

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

        self._easy_plot()

        #self._create_dataframes()
        # self._plot_all()

        # self.canvas = FigureCanvasTkAgg(self._plot_all(), master=self)
        # self.canvas.draw()
        # self.canvas.get_tk_widget().pack()


    def _create_dataframes(self):
        """Generate data frames for plots
        """
        self.df_day = self.master.user.os_tools.create_dataframe(
            self.master.user.Folder['work_daysum'], 
            self.master.user.Meter['day_meter'])
        
        self.df_night = self.master.user.os_tools.create_dataframe(
            self.master.user.Folder['work_daysum'], 
            self.master.user.Meter['night_meter'])
        
    def _easy_plot(self):
        """testplot
        """
        #self.plot_title('Tkinter Matplotlib Demo')

        # prepare data
        data = {
            'Python': 11.27,
            'C': 11.16,
            'Java': 10.46,
            'C++': 7.5,
            'C#': 5.26
        }
        languages = data.keys()
        popularity = data.values()

        # create a figure
        figure = Figure(dpi=100)
        #figure = Figure(figsize=(6, 4), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, self)

        # create axes
        axes = figure.add_subplot()

        # create the barchart
        axes.bar(languages, popularity)
        axes.set_title('Top 5 Programming Languages')
        axes.set_ylabel('Popularity')

        figure_canvas.get_tk_widget().pack(fill='both', expand=True)

    # def _plot_all(self):
    #     """Plot all data
    #     """
    #     fig = plt.figure(figsize =([30, 15]))

    #     # Gridspec Setup
    #     gs = gridspec.GridSpec(2, 2)
    #     ax = plt.subplot(gs[0, 0])
    #     gs.update(wspace = 0.1, hspace = 0.3)

    #     ### AX1 ###
    #     ax1 = plt.subplot(gs[0, :2])
    #     sns.barplot(data=self.df_day,
    #                 x='date',
    #                 y='verbrauch')
    #     ax1.set_ylabel('Verbrauch [Wh]', labelpad = 0, fontsize = 12)
    #     ax1.xaxis.set_major_locator(md.MonthLocator())
    #     ax1.xaxis.set_major_formatter(md.DateFormatter('%b'))
    #     ax1.set_title('Tagesverbrauch')

    #     ### AX2 ###
    #     ax2 = plt.subplot(gs[1, :2])
    #     sns.barplot(data=self.df_night,
    #                 x='date',
    #                 y='verbrauch')
    #     ax2.set_ylabel('Verbrauch [Wh]', labelpad = 0, fontsize = 12)
    #     ax2.xaxis.set_major_locator(md.MonthLocator())
    #     ax2.xaxis.set_major_formatter(md.DateFormatter('%b'))
    #     ax2.set_title('Nachtstrom')

    #     return fig
    
    #     # tk addidtions
    #     # canvas = FigureCanvasTkAgg(fig, master=self)
    #     # #canvas.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    #     # canvas.get_tk_widget().grid(row=0)
    #     # canvas.draw()


    #     # ### Draw Plot ###
    #     # plt.show()