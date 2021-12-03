#include <Arduino.h>
#include <SparkFun_Bio_Sensor_Hub_Library.h>
#include <Wire.h>

class Oximeter {
public:
    static const int ADDR = 0x55;   // Physical address of the device
    static const int RS = 8;   // Reset pin
    static const int MFIO = 9; // MFIO pin

    Oximeter::Oximeter();
    void setup();
    void Oximeter::write();
private:
    /**
     * @brief // Takes address, reset pin, and MFIO pin. 
     */
    SparkFun_Bio_Sensor_Hub* bioHub;
    bioData* body;
};