import time
import tkinter as tk
from time import strftime
from tkinter import N, W, E, S, BOTH

import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

class Diagnosis:
    TIME_AVERAGE = 10

    def __init__(self, diagn_frame):
        self.__diagn_frame = diagn_frame
        self.__diagn_frame.columnconfigure(0, weight=1)
        self.__diagn_frame.rowconfigure(0, weight=1)
        self.__diagn_frame.rowconfigure(1, weight=1)

        self.__avg_oxg = None
        self.__avg_hr = None
        self.__avg_temp = None
        self.__timer = Diagnosis.TIME_AVERAGE

        self.__upper_frame = tk.Frame(self.__diagn_frame, background="black")
        self.__upper_frame.grid(column=0, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky="news")
        self.__upper_frame.columnconfigure(0, weight=1)
        self.__upper_frame.rowconfigure(0, weight=1)
        self.__title_label = tk.Label(self.__upper_frame, text="Diagnosis", anchor="center",
                                      font=("Courier", 20, "bold"))
        self.__title_label.grid(column=0, row=0, sticky="news", padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES)

        self.__lower_frame = tk.Frame(self.__diagn_frame, background="black")
        self.__lower_frame.grid(column=0, row=1, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky="news")
        self.__lower_frame.columnconfigure(0, weight=1)
        self.__lower_frame.rowconfigure(0, weight=1)
        self.__lower_frame.rowconfigure(1, weight=1)

        self.__start_button = None
        self.position_button()

        self.__values_frame = tk.Label(self.__lower_frame, text="Average values still undefined", anchor="center",
                                       font=("Courier", 20))
        self.__values_frame.grid(column=0, row=1, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky="news")

    def position_button(self):
        self.__start_button = tk.Button(self.__lower_frame, text="Start diagnosis", anchor="center", font=("Courier", 10), fg="green")
        self.__start_button.config(command=lambda: self.__start_diag_handler())
        self.__start_button.grid(column=0, row=0, sticky="news", padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES)

    def __start_diag_handler(self):
        self.__start_button.grid_forget()

        self.__avg_frame = tk.Frame(self.__lower_frame, background="black")
        self.__avg_frame.grid(column=0, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky="news")
        self.__avg_frame.columnconfigure(0, weight=1)
        self.__avg_frame.rowconfigure(0, weight=1)

        # calculating average tre puntini e tra parentesi il tempo,
        # e sotto ci metto heart rate e ossigeno... poi quando finisce ci metto la diagnosis, e la media

        self.__calculating_label = tk.Label(self.__avg_frame, text="Calculating average:\nWait for a tot of seconds",
                                            anchor="center", font=("Courier", 20))
        self.__calculating_label.grid(column=0, row=0, sticky="news", padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES)
        self.start_average([], [], [], 0)

    def start_average(self, hr_array, oxg_array, temp_array, count):
        time_string = strftime('%S', time.gmtime(self.__timer))  # time format
        self.__calculating_label.config(text="Calculating average:\nWait for " + time_string + "s")
        self.__timer -= 0.1

        hr_array.append(GUI.global_oximeter.get_heart_rate())
        oxg_array.append(GUI.global_oximeter.get_oxygen())
        temp_array.append(GUI.global_thermometer.get_obj_temp())
        count += 1

        if self.__timer > 0:
            GUI.root.after(100, self.start_average, hr_array, oxg_array, temp_array, count)
        else:
            self.__timer = Diagnosis.TIME_AVERAGE
            self.__avg_hr = sum(hr_array) / count
            self.__avg_oxg = sum(oxg_array) / count
            self.__avg_temp = sum(temp_array) / count
            self.update_values_frame(GUI.global_thermometer.get_unit())
            self.__calculating_label.grid_forget()
            self.position_button()


    def update_values_frame(self, unit):
        self.__values_frame.config(text="Average values:\n"
                                        "HR: " + str(round(self.__avg_hr)) + "BPM; "
                                        " Oxg: " + str(round(self.__avg_oxg)) + "%; "
                                        " Temp: " + str(round(self.__avg_temp, 2)) + unit)

    def change_unit_avg_temp(self, unit):
        if unit == 'C':  # We passed from Fahrenheit to Celsius
            self.__avg_temp = (self.__avg_temp - 32) / 1.8
        elif unit == 'K':
            self.__avg_temp = self.__avg_temp + 273.15
        elif unit == 'F':
            self.__avg_temp = self.__avg_temp * 9 / 5 - 459.67

        self.update_values_frame(unit)


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

        self.__status = 0
        self.__oxygen = 0
        self.__confidence = 0
        self.__heart_rate = 0

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

        self.update_oxim_labels()

    def update_oxim_labels(self):
        self.__status_label.config(text="Status: " + str(self.__status))
        self.__oxygen_label.config(text="Oxygen: " + str(self.__oxygen) + "%")
        self.__confidence_label.config(text="Confidence: " + str(self.__confidence) + "%")
        self.__heart_rate_label.config(text="Heart Rate: " + str(self.__oxygen) + "BPM")

    def get_heart_rate(self):
        return self.__heart_rate

    def get_oxygen(self):
        return self.__oxygen

    def get_oxg_status(self):
        return self.__status

    def set_parameters(self, ox_status, ox_oxygen, ox_confidence, ox_heart_rate):
        if ox_status == 0:
            self.__status = "No object detected"
        elif ox_status == 1:
            self.__status = "Object detected"
        elif ox_status == 2:
            self.__status = "Object other than finger detected"
        elif ox_status == 3:
            self.__status = "Finger detected"
        self.__oxygen = ox_oxygen
        self.__confidence = ox_confidence
        self.__heart_rate = ox_heart_rate

        self.update_oxim_labels()


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
        self.__change_unit_but = tk.Button(self.__buttons_frame, text="Change\nUnit", anchor="center",
                                           font=("Courier", 10), fg="green")
        self.__change_unit_but.config(command=lambda: self.__change_unit_handler())
        self.__change_unit_but.grid(column=0, row=0, sticky="news", padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES)

        self.update_temp_labels()

    def __change_unit_handler(self):
        self.__unit = Thermometer.UNITS[(Thermometer.UNITS.index(self.__unit)) - 1]

        if self.__unit == 'C':  # We passed from Fahrenheit to Celsius
            self.__obj_temp = (self.__obj_temp - 32) / 1.8
            self.__amb_temp = (self.__amb_temp - 32) / 1.8
        elif self.__unit == 'K':
            self.__obj_temp = self.__obj_temp + 273.15
            self.__amb_temp = self.__amb_temp + 273.15
        elif self.__unit == 'F':
            self.__obj_temp = self.__obj_temp * 9 / 5 - 459.67
            self.__amb_temp = self.__amb_temp * 9 / 5 - 459.67

        self.update_temp_labels()
        GUI.global_diagnosis.change_unit_avg_temp(self.__unit)

    def bind_to_change_unit_button(self, callback):
        self.__change_unit_callbacks.append(callback)

    def update_temp_labels(self):
        obj_text = "Obj T: " + str(round(self.__obj_temp, 2)) + " " + self.__unit
        amb_temp = "Amb T: " + str(round(self.__amb_temp, 2)) + " " + self.__unit
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

    def get_obj_temp(self):
        return self.__obj_temp

    def get_unit(self):
        return self.__unit

class Plot:
    """This class controls each chart of the application"""

    def __init__(self, fontsize, plot_frame, y_label, ylim):
        self.__figure = Figure(dpi=fontsize)
        self.__subplot = self.__figure.add_subplot(111)
        self.__LEN_ARRAY = GUI.POINTS_NUMBER

        self.__points = []

        self.__canvas = FigureCanvasTkAgg(self.__figure, master=plot_frame)  # A tk.DrawingArea.
        self.__canvas.draw()
        self.__canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # self.__subplot.set_title("title")
        self.__subplot.set_xlabel("Time")
        self.__subplot.set_ylabel(y_label)
        self.__subplot.set_ylim(ylim[0], ylim[1])
        self.__subplot.set_xticks([])

        # It's necessary to avoid clearing also labels and titles with subplot.clear()
        # https://stackoverflow.com/questions/60598164/how-do-i-change-the-subplot-parameters-having-a-figure-in-a-window-in-tkinter
        self.__line, = self.__subplot.plot([], [])

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
        self.__line.set_data(x_array, self.__points)
        self.__subplot.relim()  # recalculate limits
        self.__subplot.autoscale_view(True, True, True)  # rescale using limits

    def get_figure(self):
        return self.__figure


class GUI:
    """This class gives the basis for building the GUI. It defines the main frames, their position and their style"""

    global_diagnosis = None
    global_thermometer = None
    global_oximeter = None
    POINTS_NUMBER = 50
    PLOT_FONT_SIZE = 100
    SIZE_GRID = 12
    APP_TITLE = "-- DEFINE TITLE --"
    WINDOW_GEOMETRY = "1200x800"
    PAD_BTW_FRAMES = 10  # Padding between frames
    DARK_RED = "#ab2800"
    root = None

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
        GUI.root = self.__root = root

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
        self.__control_frame.grid(column=0, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky="news")
        self.__control_frame.columnconfigure(0, weight=1)
        self.__control_frame.rowconfigure(0, weight=1)
        self.__control_frame.rowconfigure(1, weight=2)
        self.__control_frame.rowconfigure(2, weight=2)

        # Thermometer frame setup
        self.__thermo_frame = tk.Frame(self.__control_frame, background="red")
        self.__thermo_frame.grid(column=0, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky="news")
        GUI.global_thermometer = self.__thermometer = Thermometer(self.__thermo_frame)

        # Oximeter frame setup
        self.__oxim_frame = tk.Frame(self.__control_frame, background="red")
        self.__oxim_frame.grid(column=0, row=1, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky="news")
        GUI.global_oximeter = self.__oximeter = Oximeter(self.__oxim_frame)

        # Average frame setup
        self.__diagnosis_frame = tk.Frame(self.__control_frame, background="red")
        self.__diagnosis_frame.grid(column=0, row=2, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky="news")
        GUI.global_diagnosis = self.__diagnosis_frame = Diagnosis(self.__diagnosis_frame)

        # Plots frame setup
        self.__plots_frame = tk.Frame(self.__mainframe, background=GUI.DARK_RED)
        self.__plots_frame.grid(column=1, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky="news")
        self.__plots_frame.columnconfigure(0, weight=1)
        self.__plots_frame.rowconfigure(0, weight=1)
        self.__plots_frame.rowconfigure(1, weight=1)

        # Top plot frame setup
        self.__top_plot_frame = tk.Frame(self.__plots_frame, background="black")
        self.__top_plot_frame.grid(column=0, row=0, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky="news")
        self.__top_plot_frame.columnconfigure(0, weight=1)
        self.__top_plot_frame.rowconfigure(0, weight=1)
        self.__top_plot = Plot(GUI.PLOT_FONT_SIZE, self.__top_plot_frame, "Heart Rate [BPM]", [50, 180])

        # Bottom plot frame setup
        self.__bottom_plot_frame = tk.Frame(self.__plots_frame, background="black")
        self.__bottom_plot_frame.grid(column=0, row=1, padx=GUI.PAD_BTW_FRAMES, pady=GUI.PAD_BTW_FRAMES, sticky="news")
        self.__bottom_plot_frame.columnconfigure(0, weight=1)
        self.__bottom_plot_frame.rowconfigure(0, weight=1)
        self.__bottom_plot = Plot(GUI.PLOT_FONT_SIZE, self.__bottom_plot_frame, "Oxygen Saturation [%]", [92, 100])

    def bind_callback(self, callback):
        """This method binds a callback to the GUI. It enables the pattern Observer-Observable"""
        self.__callbacks.append(callback)

    def get_top_plot(self):
        return self.__top_plot

    def get_bottom_plot(self):
        return self.__bottom_plot

    def get_thermometer(self):
        return self.__thermometer

    def get_oximeter(self):
        return self.__oximeter

    def add_charts_points(self, ox_heart_rate, ox_oxygen):
        self.__bottom_plot.append_point(ox_oxygen)
        self.__top_plot.append_point(ox_heart_rate)
