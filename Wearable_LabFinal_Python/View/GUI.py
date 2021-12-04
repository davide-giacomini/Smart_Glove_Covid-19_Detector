import tkinter as tk
from tkinter import N, W, E, S, BOTH

import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

class Oximeter:
    """This class displays oximeter values"""
    def __init__(self, oxim_frame):
        self.__oxim_frame = oxim_frame

class Thermometer:
    """This class displays the themperature values"""
    def __init__(self, thermo_frame):
        self.__thermo_frame = thermo_frame
        self.__thermo_frame.columnconfigure(0, weight=7)
        self.__thermo_frame.columnconfigure(1, weight=3)
        self.__thermo_frame.rowconfigure(0, weight=1)
        self.__thermo_frame.rowconfigure(1, weight=1)

        # Object temperature label
        self.__control_frame = tk.Frame(self.__thermo_frame, background="black")
        self.__control_frame.grid(column=0, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES,
                                  sticky=(N, W, S, E))
        self.__control_frame.columnconfigure(0, weight=1)
        self.__control_frame.rowconfigure(0, weight=1)
        self.__control_label = tk.Label(self.__control_frame, anchor="c", font=("Courier", 30))
        self.__control_label.grid(column=0, row=2, sticky="news", padx=60, pady=60)

        # Ambient temperature label
        self.__control_frame = tk.Frame(self.__thermo_frame, background="black")
        self.__control_frame.grid(column=0, row=1, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES,
                                  sticky=(N, W, S, E))
        self.__control_frame.columnconfigure(0, weight=1)
        self.__control_frame.rowconfigure(0, weight=1)

        # Ambient temperature label
        self.__control_frame = tk.Frame(self.__thermo_frame, background="black")
        self.__control_frame.grid(column=0, row=1, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES,
                                  sticky=(N, W, S, E))
        self.__control_frame.columnconfigure(0, weight=1)
        self.__control_frame.rowconfigure(0, weight=1)

        # Unit button
        self.__change_unit_but = tk.Button(self.__thermo_frame, text="Change Unit", anchor="c", font=("Courier", 10), fg="green")
        # self.__play_pause_button.config(command=lambda: controller.play_pause_callback(self.__play_pause_button))
        self.__change_unit_but.grid(column=1, row=0, sticky="news", padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES)


class Plot:
    """This class controls each chart of the application"""

    def __init__(self, fontsize, plot_frame):
        self.__figure = Figure(dpi=fontsize)
        self.__subplot = self.__figure.add_subplot(111)
        self.__LEN_ARRAY = GUI.POINTS_NUMBER

        self.__points = []

        self.__canvas = FigureCanvasTkAgg(self.__figure, master=plot_frame)  # A tk.DrawingArea.
        self.__canvas.draw()
        self.__canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def append_point(self, point):
        """It appends a new point to the chart. If the chart is already full, it slides towards the left."""
        if len(self.__points) < self.__LEN_ARRAY:
            self.__points.append(point)
            return

        self.__points.pop(0)
        self.__points.append(point)

    def animate(self, i):
        """It lets the application receive live updates (code adapted by https://www.youtube.com/watch?v=JQ7QP5rPvjU)"""
        x_array = np.arange(0, len(self.__points), 1)
        self.__subplot.clear()
        self.__subplot.plot(x_array, self.__points)

    def get_figure(self):
        return self.__figure


class GUI:
    """This class gives the basis for building the GUI. It defines the main frames, their position and their style"""

    POINTS_NUMBER = 200
    PLOT_FONT_SIZE = 100
    SIZE_GRID = 12
    APP_TITLE = "-- DEFINE TITLE --"
    WINDOW_GEOMETRY = "1200x800"
    PAD_BTW_FRAMES = 10  # Padding between frames
    DARK_RED = "#ab2800"

    def update_observers(self, *args):
        """This method will call the functions put in the array by the observers of the class GUI"""
        for callback in self.__callbacks:
            callback(args)

    def __init__(self, root, *args, **kwargs):
        """
        This method initializes all frames of Tkinter and the corresponding classes
        A sketch of all the components is in the documentation file TODO: decide where to put doc file and do it
        """
        self.__callbacks = []   # Callbacks put here by the observers to manage changes in the GUI
        self.__root = root

        root.title(GUI.APP_TITLE)
        root.geometry(GUI.WINDOW_GEOMETRY)

        # Main frame setup
        self.__mainframe = tk.Frame(root)
        self.__mainframe.grid(column=0, row=0)
        self.__mainframe.pack(fill=BOTH, expand=True)
        self.__mainframe.columnconfigure(0, weight=3)
        self.__mainframe.columnconfigure(1, weight=7)
        self.__mainframe.rowconfigure(0, weight=1)

        # Control frame setup
        self.__control_frame = tk.Frame(self.__mainframe, background="black")
        self.__control_frame.grid(column=0, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES,
                                  sticky=(N, W, S, E))
        self.__control_frame.columnconfigure(0, weight=1)
        self.__control_frame.rowconfigure(0, weight=1)
        self.__control_frame.rowconfigure(1, weight=1)

        # Thermometer frame setup
        self.__thermo_frame = tk.Frame(self.__control_frame, background="red")
        self.__thermo_frame.grid(column=0, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES,
                                  sticky=(N, W, S, E))
        self.__thermometer = Thermometer(self.__thermo_frame)

        # Oximeter frame setup
        self.__oxim_frame = tk.Frame(self.__control_frame, background="red")
        self.__oxim_frame.grid(column=0, row=1, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES,
                                  sticky=(N, W, S, E))
        self.__oximeter = Oximeter(self.__oxim_frame)


        # Plots frame setup
        self.__plots_frame = tk.Frame(self.__mainframe, background=GUI.DARK_RED)
        self.__plots_frame.grid(column=1, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky=(N, W, S, E))
        self.__plots_frame.columnconfigure(0, weight=1)
        self.__plots_frame.rowconfigure(0, weight=1)
        self.__plots_frame.rowconfigure(1, weight=1)

        # Top plot frame setup
        self.__top_plot_frame = tk.Frame(self.__plots_frame, background="black")
        self.__top_plot_frame.grid(column=0, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES,
                                   sticky=(N, W, S, E))
        self.__top_plot_frame.columnconfigure(0, weight=1)
        self.__top_plot_frame.rowconfigure(0, weight=1)
        self.__top_plot = Plot(GUI.PLOT_FONT_SIZE, self.__top_plot_frame)

        # Bottom plot frame setup
        self.__bottom_plot_frame = tk.Frame(self.__plots_frame, background="black")
        self.__bottom_plot_frame.grid(column=0, row=1, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES,
                                      sticky=(N, W, S, E))
        self.__bottom_plot_frame.columnconfigure(0, weight=1)
        self.__bottom_plot_frame.rowconfigure(0, weight=1)
        self.__bottom_plot = Plot(GUI.PLOT_FONT_SIZE, self.__bottom_plot_frame)

    def bind_callback(self, callback):
        """This method binds a callback to the GUI. It enables the pattern Observer-Observable"""
        self.__callbacks.append(callback)

    def get_top_plot(self):
        return self.__top_plot

    def get_bottom_plot(self):
        return self.__bottom_plot
