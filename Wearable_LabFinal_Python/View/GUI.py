import tkinter as tk
from tkinter import N, W, E, S, BOTH, NW, NE, SW
import matplotlib as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class Plot:
    def __init__(self, fontsize, plot_frame):
        self.__figure = Figure(dpi=fontsize)
        self.__LEN_ARRAY = GUI.POINTS_NUMBER
        self.__points = []

        self.__canvas = FigureCanvasTkAgg(self.__figure, master=plot_frame)  # A tk.DrawingArea.
        self.__canvas.draw()
        self.__canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot(self):
        for point in range(len(self.__points)):
            self.__figure.add_subplot(111).plot(point, self.__points[point])

    def append_point(self, point):
        if len(self.__points) < self.__LEN_ARRAY:
            self.__points.append(point)
            return

        self.__points.pop(0)
        self.__points.append(point)


class GUI:
    """This class gives the basis for building the GUI. It defines the main frames, their position and their style"""

    POINTS_NUMBER = 10
    PLOT_FONT_SIZE = 100
    SIZE_GRID = 12
    APP_TITLE = "-- DEFINE TITLE --"
    WINDOW_GEOMETRY = "1200x800"
    PAD_BTW_FRAMES = 10  # Padding between frames
    DARK_RED = "#ab2800"

    def update_observers_button(self, button):
        for observer in self.__observers:
            observer.update_button(button)

    def __init__(self, root, *args, **kwargs):
        self.__observers = []
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
        self.__control_frame.grid(column=0, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky=(N, W, S, E))
        self.__control_frame.columnconfigure(0, weight=1)
        self.__control_frame.rowconfigure(0, weight=1)

        # Plots frame setup
        self.__plots_frame = tk.Frame(self.__mainframe, background=GUI.DARK_RED)
        self.__plots_frame.grid(column=1, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky=(N, W, S, E))
        self.__plots_frame.columnconfigure(0, weight=1)
        self.__plots_frame.rowconfigure(0, weight=1)
        self.__plots_frame.rowconfigure(1, weight=1)

        # Top plot frame setup
        self.__top_plot_frame = tk.Frame(self.__plots_frame, background="black")
        self.__top_plot_frame.grid(column=0, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky=(N, W, S, E))
        self.__top_plot_frame.columnconfigure(0, weight=1)
        self.__top_plot_frame.rowconfigure(0, weight=1)
        self.__top_plot = Plot(GUI.PLOT_FONT_SIZE, self.__top_plot_frame)

        # Bottom plot frame setup
        self.__bottom_plot_frame = tk.Frame(self.__plots_frame, background="black")
        self.__bottom_plot_frame.grid(column=0, row=1, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky=(N, W, S, E))
        self.__bottom_plot_frame.columnconfigure(0, weight=1)
        self.__bottom_plot_frame.rowconfigure(0, weight=1)
        self.__bottom_plot = Plot(GUI.PLOT_FONT_SIZE, self.__bottom_plot_frame)

    def bind_to(self, observer):
        self.__observers.append(observer)

    def get_top_plot(self):
        return self.__top_plot

    def get_bottom_plot(self):
        return self.__bottom_plot
