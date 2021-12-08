#include "oximeter.h"

Oximeter::Oximeter()
{
    // Takes address, reset pin, and MFIO pin.
    Oximeter::bioHub = new SparkFun_Bio_Sensor_Hub(Oximeter::RS, Oximeter::MFIO);
}

void Oximeter::setup()
{
    int result = Oximeter::bioHub->begin();
    if (!result)
        Serial.println("Sensor started!");
    else
        Serial.println("Could not communicate with the sensor!!!");

    Serial.println("Configuring Sensor....");
    int error = Oximeter::bioHub->configBpm(MODE_ONE); // Configuring just the BPM settings.
    if (!error)
    {
        Serial.println("Sensor configured.");
    }
    else
    {
        Serial.println("Error configuring sensor.");
        Serial.print("Error: ");
        Serial.println(error);
    }
    // Data lags a bit behind the sensor, if you're finger is on the sensor when
    // it's being configured this delay will give some time for the data to catch
    // up.
}

bioData Oximeter::getBioData()
{

    return Oximeter::bioHub->readBpm();
}