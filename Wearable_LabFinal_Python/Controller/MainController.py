import random
import time
import tkinter as tk
import matplotlib.animation as anim

import serial

import View.GUI as g

# Our application will have to communicate with Arduino at the port 115200 of the serial monitor.
# The board is the ATMEGA328P, aka Arduino Pro or Pro Mini ATmega328 (https://docs.platformio.org/en/latest/boards/atmelavr/pro8MHzatmega328.html)

try:
    ser = serial.Serial('/dev/ttyACM0', 115200)  # Create Serial port object called ArduinoUnoSerialData time.sleep(2)
except:
    print("Serial connection impossible to initialize.")


class MainController:
    """This class controls the entire application. It's standalone because it's a simple application"""

    def __init__(self, gui):
        self.__gui = gui
        self.__gui.bind_callback(self.update_button)

    def get_gui(self):
        return self.__gui

    def update_button(self, *args):
        pass


if __name__ == "__main__":
    root_frame = tk.Tk()
    gui = g.GUI(root_frame)
    main_controller = MainController(gui)

    # TODO improve these two calls. I would like to call the function `animate` inside the class `Plot`,
    #  but it no more updates if I do it. It seems like the reference to an1 and an2 get lost for garbage collection.
    #  Fixing this problem would bring to a cleaner and more maintainable code.
    an1 = anim.FuncAnimation(gui.get_top_plot().get_figure(), gui.get_top_plot().animate, interval=100)
    an2 = anim.FuncAnimation(gui.get_bottom_plot().get_figure(), gui.get_bottom_plot().animate, interval=100)

    # Update gui window
    root_frame.update_idletasks()
    root_frame.update()

    # Check the serial monitor and then update the gui window forever.
    # Note: this is a unique-thread method for implementing a non-blocking wait for the serial monitor input.
    # A multiple-thread method could have been used and it would have been more generic, but it's not necessary
    # in this case. `root_frame.mainloop()` would be blocking and there would be no way to check the serial
    # monitor. These two methods are not blocking, hence the serial monitor is indefinitely checked.
    while True:
        # Check the serial monitor
        try:
            if ser.in_waiting:
                line = ser.readline().decode("utf-8")
                values = line.split("+")
                obj_temp_F = float(values[0])
                obj_temp_C = float(values[1])
                obj_temp_K = float(values[2])
                amb_temp_F = float(values[3])
                amb_temp_C = float(values[4])
                amb_temp_K = float(values[5])
                ox_status = int(values[6])
                ox_oxygen = int(values[7])
                ox_confidence = int(values[8])
                ox_heart_rate = float(values[9])
                gui.get_thermometer().set_temp(obj_temp_F, obj_temp_C, obj_temp_K, amb_temp_F, amb_temp_C, amb_temp_K)
                gui.get_oximeter().set_parameters(ox_status, ox_oxygen, ox_confidence, ox_heart_rate)
        except Exception as err:
            # print(Exception, err)
            pass

        # TODO remove next three lines (debug)
        gui.get_top_plot().append_point(random.randint(-10, 10))
        gui.get_bottom_plot().append_point(random.randint(-10, 10))
        time.sleep(0.01)

        # Update gui window forever
        root_frame.update_idletasks()
        root_frame.update()
