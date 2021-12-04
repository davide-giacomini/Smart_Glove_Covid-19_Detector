#include <Arduino.h>
#include <Wire.h> // I2C library, required for MLX90614
#include <SparkFunMLX90614.h> //Click here to get the library: http://librarymanager/All#Qwiic_IR_Thermometer by SparkFun

class Thermometer {
public:
    static const int ADDR = 0x5A;

    Thermometer::Thermometer();
    /**
     * @brief It sets up the device (default temperature is Fahrenheit)
     * 
     */
    bool setup();

    /**
     * @brief It returns the object temperature in °C, if readable. If it's not
     * readable, it returns -1
     * 
     * @return float returns the object temperature in °C, if readable. If it's not
     * readable, it returns -1
     */
    float Thermometer::getCelsiusObject();
    /**
     * @brief It returns the ambient temperature in °C, if readable. If it's not
     * readable, it returns -1
     * 
     * @return float returns the ambient temperature in °C, if readable. If it's not
     * readable, it returns -1
     */
    float Thermometer::getCelsiusAmbient();
    /**
     * @brief It returns the object temperature in °F, if readable. If it's not
     * readable, it returns -1
     * 
     * @return float returns the object temperature in °F, if readable. If it's not
     * readable, it returns -1
     */
    float Thermometer::getFahrenheitObject();
    /**
     * @brief It returns the ambient temperature in °F, if readable. If it's not
     * readable, it returns -1
     * 
     * @return float returns the ambient temperature in °F, if readable. If it's not
     * readable, it returns -1
     */
    float Thermometer::getFahrenheitAmbient();
    /**
     * @brief It returns the object temperature in K, if readable. If it's not
     * readable, it returns -1
     * 
     * @return float returns the object temperature in K, if readable. If it's not
     * readable, it returns -1
     */
    float Thermometer::getKelvinObject();
    /**
     * @brief It returns the ambient temperature in K, if readable. If it's not
     * readable, it returns -1
     * 
     * @return float returns the ambient temperature in K, if readable. If it's not
     * readable, it returns -1
     */
    float Thermometer::getKelvinAmbient();
    void write();
private:
    IRTherm* thermometer;
};