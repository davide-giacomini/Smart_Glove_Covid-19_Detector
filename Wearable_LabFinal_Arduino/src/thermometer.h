#include <Arduino.h>
#include <Wire.h> // I2C library, required for MLX90614
#include <SparkFunMLX90614.h> //Click here to get the library: http://librarymanager/All#Qwiic_IR_Thermometer by SparkFun

class Thermometer {
public:
    static const int ADDR = 0x5A;

    Thermometer::Thermometer();
    void setup();
    void write();
private:
    IRTherm* thermometer;
};