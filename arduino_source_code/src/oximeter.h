#include <Arduino.h>
#include <SparkFun_Bio_Sensor_Hub_Library.h>
#include <Wire.h>

enum class OximeterStatus {
    NO_OBJ = 0,
    OBJ_DET = 1,
    OBJ_NO_FIN_DET = 2,
    FING_DET = 3
};

/**
 * @brief This class encapsulates the Oximeter information
 * 
 */
class Oximeter {
public:
    static const int ADDR = 0x55;   // Physical address of the device
    static const int RS = 8;   // Reset pin
    static const int MFIO = 9; // MFIO pin

    Oximeter::Oximeter();
    void setup();
    /**
     * @brief This getter is necessary to get the bioData object from the SparkFun_Bio_Sensor_Hub_Library library.
     * Getting the reference would result in spurious values (still don't know why)
     * 
     * @return a bioData object, that contains all the values in which we are interested from the oximeter
     */
    const bioData Oximeter::getBioData();
private:
    /**
     * @brief // Takes address, reset pin, and MFIO pin. 
     */
    SparkFun_Bio_Sensor_Hub* bioHub;
};