# Smart Glove Detector

This is an implementation of a Smart Glove that can detect internal temperature and oxygen saturation of a patient, as well as giving small diagnoses based on those values.

## Description

We developed an embedded system as a glove capable of detecting internal temperature and oxygen saturation of a patient, and displaying those values. The glove is able to work without any laptop, but comes with a graphical user interface as an additional tool. Thanks to the GUI, the glove is able to send via a serial communication more data than how much is able to display on the LCD screen positioned on the top of the glove.

<p align="center">
    <img src="assets/doctor-diagnosis.jpg" alt="doctor" style="width:500px;"/>
</p>

## Developing

The source code is available under the folders `*_source_code`, depending on which programming language it is.

The GUI written in python should be re-written by scratch. We focused on developing a good JavaFX GUI.

To better understand what and how we did, please consult the report [here](project_report/Wearable-Final-Paper.pdf)