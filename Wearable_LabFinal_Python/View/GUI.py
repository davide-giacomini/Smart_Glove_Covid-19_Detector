import tkinter as tk
from tkinter import N, W, E, S, BOTH

import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure


class Oximeter:
    """This class displays oximeter values"""

    def __init__(self, oxim_frame):
        self.__oxim_frame = oxim_frame
        self.__oxim_frame.columnconfigure(0, weight=1)
        self.__oxim_frame.rowconfigure(0, weight=1)
        self.__oxim_frame.rowconfigure(1, weight=1)
        self.__oxim_frame.rowconfigure(2, weight=1)
        self.__oxim_frame.rowconfigure(3, weight=1)
        self.__oxim_frame.rowconfigure(4, weight=1)

        self.__title_label = tk.Label(self.__oxim_frame, text="Oximeter parameters", anchor="center",
                                      font=("Courier", 20))
        self.__title_label.grid(column=0, row=0, sticky="news", padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES)

        self.__status_label = tk.Label(self.__oxim_frame, text="Status", anchor="center",
                                       font=("Courier", 15))
        self.__status_label.grid(column=0, row=1, sticky="news", padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES)

        self.__oxygen_label = tk.Label(self.__oxim_frame, text="Oxygen", anchor="center",
                                       font=("Courier", 15))
        self.__oxygen_label.grid(column=0, row=2, sticky="news", padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES)

        self.__confidence_label = tk.Label(self.__oxim_frame, text="Confidence", anchor="center",
                                           font=("Courier", 15))
        self.__confidence_label.grid(column=0, row=3, sticky="news", padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES)

        self.__heart_rate_label = tk.Label(self.__oxim_frame, text="Heart Rate", anchor="center",
                                           font=("Courier", 15))
        self.__heart_rate_label.grid(column=0, row=4, sticky="news", padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES)


class Thermometer:
    """This class displays the themperature values"""
    UNITS = ('K', 'C', 'F')

    def __init__(self, thermo_frame):
        self.__thermo_frame = thermo_frame
        self.__thermo_frame.columnconfigure(0, weight=1)
        self.__thermo_frame.rowconfigure(0, weight=1)
        self.__thermo_frame.rowconfigure(1, weight=2)

        self.__change_unit_callbacks = []
        self.__unit = 'F'  # Can be F, C or K
        self.__obj_temp = 0  # Temperature initialized at zero
        self.__amb_temp = 0  # Temperature initialized at zero

        self.__title_frame = tk.Frame(self.__thermo_frame)
        self.__title_frame.grid(column=0, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES,
                                sticky=(N, W, S, E))
        self.__title_frame.columnconfigure(0, weight=1)
        self.__title_frame.rowconfigure(0, weight=1)
        self.__title_label = tk.Label(self.__title_frame, text="Thermometer parameters", anchor="center",
                                      font=("Courier", 20))
        self.__title_label.grid(column=0, row=0, sticky="news", padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES)

        self.__content_frame = tk.Frame(self.__thermo_frame)
        self.__content_frame.grid(column=0, row=1, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES,
                                  sticky=(N, W, S, E))
        self.__content_frame.columnconfigure(0, weight=7)
        self.__content_frame.columnconfigure(1, weight=3)
        self.__content_frame.rowconfigure(0, weight=1)

        self.__labels_frame = tk.Frame(self.__content_frame)
        self.__labels_frame.grid(column=0, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES,
                                 sticky=(N, W, S, E))
        self.__labels_frame.columnconfigure(0, weight=1)
        self.__labels_frame.rowconfigure(0, weight=1)
        self.__labels_frame.rowconfigure(1, weight=1)
        self.__labels_frame.rowconfigure(2, weight=1)

        self.__buttons_frame = tk.Frame(self.__content_frame)
        self.__buttons_frame.grid(column=1, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES,
                                  sticky=(N, W, S, E))
        self.__buttons_frame.columnconfigure(0, weight=1)
        self.__buttons_frame.rowconfigure(0, weight=1)

        # Object temperature label
        # self.__obj_temp_frame = tk.Frame(self.__thermo_frame)
        # self.__obj_temp_frame.grid(column=0, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES,
        #                           sticky=(N, W, S, E))
        # self.__obj_temp_frame.columnconfigure(0, weight=1)
        # self.__obj_temp_frame.rowconfigure(0, weight=1)
        self.__obj_temp_label = tk.Label(self.__labels_frame, text="Object Temperature", anchor="center",
                                         font=("Courier", 15))
        self.__obj_temp_label.grid(column=0, row=1, sticky="news", padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES)

        # Ambient temperature label
        # self.__amb_temp_frame = tk.Frame(self.__thermo_frame)
        # self.__amb_temp_frame.grid(column=0, row=1, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES,
        #                           sticky=(N, W, S, E))
        # self.__amb_temp_frame.columnconfigure(0, weight=1)
        # self.__amb_temp_frame.rowconfigure(0, weight=1)
        self.__amb_temp_label = tk.Label(self.__labels_frame, text="Ambient Temperature", anchor="center",
                                         font=("Courier", 15))
        self.__amb_temp_label.grid(column=0, row=2, sticky="news", padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES)

        # Unit button
        self.__change_unit_but = tk.Button(self.__buttons_frame, text="Change Unit", anchor="center",
                                           font=("Courier", 10), fg="green")
        self.__change_unit_but.config(command=lambda: self.__change_unit_handler())
        self.__change_unit_but.grid(column=0, row=0, sticky="news", padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES)

    def __change_unit_handler(self):
        self.__unit = Thermometer.UNITS[(Thermometer.UNITS.index(self.__unit)) - 1]

        if self.__unit == 'C':  # We passed from Fahrenheit to Celsius
            self.__obj_temp = (self.__obj_temp - 32) / 1.8
            self.__amb_temp = (self.__obj_temp - 32) / 1.8
        elif self.__unit == 'K':
            self.__obj_temp = self.__obj_temp + 273.15
            self.__amb_temp = self.__obj_temp + 273.15
        elif self.__unit == 'F':
            self.__obj_temp = self.__obj_temp * 9 / 5 - 459.67
            self.__amb_temp = self.__obj_temp * 9 / 5 - 459.67

        self.update_temp_labels()

    def bind_to_change_unit_button(self, callback):
        self.__change_unit_callbacks.append(callback)

    def update_temp_labels(self):
        obj_text = "Obj T: " + str(self.__obj_temp) + " " + self.__unit
        amb_temp = "Amb T: " + str(self.__amb_temp) + " " + self.__unit
        self.__obj_temp_label.config(text=obj_text)
        self.__amb_temp_label.config(text=amb_temp)

    def set_temp(self, obj_temp_F, obj_temp_C, obj_temp_K, amb_temp_F, amb_temp_C, amb_temp_K):
        if self.__unit == 'F':
            self.__obj_temp = obj_temp_F
            self.__amb_temp = amb_temp_F
        elif self.__unit == 'C':
            self.__obj_temp = obj_temp_C
            self.__amb_temp = amb_temp_C
        elif self.__unit == 'K':
            self.__obj_temp = obj_temp_K
            self.__amb_temp = amb_temp_K

        self.update_temp_labels()

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
        self.__callbacks = []  # Callbacks put here by the observers to manage changes in the GUI
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

    def get_thermometer(self):
        return self.__thermometer
