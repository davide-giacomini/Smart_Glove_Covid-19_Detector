#include "thermometer.h"

Thermometer::Thermometer() {
    Thermometer::thermometer = new IRTherm();
}

void Thermometer::setup() {
    // Wire.beginTransmission(Thermometer::ADDR); //Joing I2C bus
    
    if (Thermometer::thermometer->begin() == false){ // Initialize thermal IR sensor
        Serial.println("Qwiic IR thermometer did not acknowledge! Freezing!");
        while(1);
    }
    Serial.println("Qwiic IR Thermometer did acknowledge.");
    
    Thermometer::thermometer->setUnit(TEMP_F); // Set the library's units to Farenheit
    // Alternatively, TEMP_F can be replaced with TEMP_C for Celsius or
    // TEMP_K for Kelvin.
    
    pinMode(LED_BUILTIN, OUTPUT); // LED pin as output

    // Wire.endTransmission();
}

void Thermometer::write() {
    digitalWrite(LED_BUILTIN, HIGH);
    
    // Call therm.read() to read object and ambient temperatures from the sensor.
    if (Thermometer::thermometer->read()) // On success, read() will return 1, on fail 0.
    {
        // Use the object() and ambient() functions to grab the object and ambient
        // temperatures.
        // They'll be floats, calculated out to the unit you set with setUnit().
        Serial.print("Object: " + String(Thermometer::thermometer->object(), 2));
        Serial.println("F");
        Serial.print("Ambient: " + String(Thermometer::thermometer->ambient(), 2));
        Serial.println("F");
        Serial.println();
    }
    digitalWrite(LED_BUILTIN, LOW);
}