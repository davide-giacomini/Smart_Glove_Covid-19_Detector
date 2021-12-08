#include "thermometer.h"

Thermometer::Thermometer()
{
    Thermometer::thermometer = new IRTherm();
}

bool Thermometer::setup()
{

    if (Thermometer::thermometer->begin() == false) // Initialize thermal IR sensor
        return false;

    // Otherwise the device is set up
    Thermometer::thermometer->setUnit(TEMP_F); // Set the library's units to Farenheit
    // Alternatively, TEMP_F can be replaced with TEMP_C for Celsius or
    // TEMP_K for Kelvin.

    pinMode(LED_BUILTIN, OUTPUT); // LED pin as output

    return true;
}

float Thermometer::getCelsiusObject()
{
    // digitalWrite(LED_BUILTIN, HIGH);
    Thermometer::thermometer->setUnit(TEMP_C);
    if (Thermometer::thermometer->read())
        return Thermometer::thermometer->object();
    else
        return -1;
    // digitalWrite(LED_BUILTIN, LOW);
}

float Thermometer::getCelsiusAmbient()
{
    Thermometer::thermometer->setUnit(TEMP_C);
    if (Thermometer::thermometer->read())
        return Thermometer::thermometer->ambient();
    else
        return -1;
}

float Thermometer::getFahrenheitObject()
{
    Thermometer::thermometer->setUnit(TEMP_F);
    if (Thermometer::thermometer->read())
        return Thermometer::thermometer->object();
    else
        return -1;
}

float Thermometer::getFahrenheitAmbient()
{
    Thermometer::thermometer->setUnit(TEMP_F);
    if (Thermometer::thermometer->read())
        return Thermometer::thermometer->ambient();
    else
        return -1;
}

float Thermometer::getKelvinObject()
{
    Thermometer::thermometer->setUnit(TEMP_K);
    if (Thermometer::thermometer->read())
        return Thermometer::thermometer->object();
    else
        return -1;
}

float Thermometer::getKelvinAmbient()
{
    Thermometer::thermometer->setUnit(TEMP_K);
    if (Thermometer::thermometer->read())
        return Thermometer::thermometer->ambient();
    else
        return -1;
}