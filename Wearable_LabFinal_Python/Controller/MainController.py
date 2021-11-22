import random
import time
import tkinter as tk

import serial

import View.GUI as g

try:
    ser = serial.Serial('/dev/ttyACM0', 115200)  # Create Serial port object called ArduinoUnoSerialData time.sleep(2)
except:
    print("Serial connection impossible to initialize.")


class MainController:
    def __init__(self, gui):
        self.__gui = gui
        self.__gui.bind_to(self)

    def get_gui(self):
        return self.__gui

    def update_button(self, button):
        pass


if __name__ == "__main__":
    root_frame = tk.Tk()
    gui = g.GUI(root_frame)
    main_controller = MainController(gui)

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
                print(line)
        except:
            pass

        # gui.get_top_plot().append_point(random.randint(-10, 10))
        # gui.get_top_plot().plot()
        gui.get_bottom_plot().append_point(random.randint(-10, 10))
        gui.get_bottom_plot().plot()

        time.sleep(1)

        # Update gui window forever
        root_frame.update_idletasks()
        root_frame.update()
