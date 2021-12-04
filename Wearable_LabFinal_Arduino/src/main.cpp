#include <Arduino.h>
#include "lcd.h"
#include "oximeter.h"
#include "thermometer.h"

#define USER_AGE 23
#define MAX_HR 220-23

// WARNING: I initially did `LCD lcd()`, but it doesn't work because the compiler messes something up with the order of constructors call. The issue and solutions are well documented here: https://arduino.stackexchange.com/questions/23168/library-liquidcrystal-i2c-dont-work-in-other-class-composition/23240
LCD *lcd;
Thermometer *thermometer;
Oximeter *oximeter;

// FIXME: Oximeter hardcoded
const int resPin = 8;
const int mfioPin = 9;
// Takes address, reset pin, and MFIO pin.
SparkFun_Bio_Sensor_Hub bioHub(resPin, mfioPin); 
bioData body;


void setup() {
  Serial.begin(115200);
  Wire.begin();

  lcd = new LCD(); // It's the same of `lcd = &LCD()` 
  lcd->setup_lcd();

  // oximeter = new Oximeter();
  // oximeter->setup();
  //FIXME: OXIMETER hardcoded
  int result = bioHub.begin();
  if (!result)
    Serial.println("Sensor started!");
  else
    Serial.println("Could not communicate with the sensor!!!");

  Serial.println("Configuring Sensor...."); 
  int error = bioHub.configBpm(MODE_ONE); // Configuring just the BPM settings. 
  if(!error){
    Serial.println("Sensor configured.");
  }
  else {
    Serial.println("Error configuring sensor.");
    Serial.print("Error: "); 
    Serial.println(error); 
  }
  // Data lags a bit behind the sensor, if you're finger is on the sensor when
  // it's being configured this delay will give some time for the data to catch
  // up. 
  // delay(4000);

  thermometer = new Thermometer();
  if (!thermometer->setup()) {
    lcd->display_error("Issue thermom");
    Serial.println("Thermometer didn't set up correctly");
  }
}

int readOxy() {
  int o = 68; // TODO check oximeter read
  return o;
}

float readTemp() {
  float t = 93; // TODO check temp read
  return t;
}

float readHB() {
  float hb = 57; // TODO check heartbeat read
  return hb;
}

void sendOxy(int o) { // TODO send data function send everything in one function
  Serial.print(o);
}

void sendTemp(float t) {
  Serial.print("+");
  Serial.print(t);
}

void sendHB(float hb) {
  Serial.print("+");
  Serial.println(hb);
}

void loop() {

  // FIXME: check if thermometer working
  float obj_temp = thermometer->getFahrenheitObject();

  // oximeter->write();
  //FIXME: OXIMETER hardcoded
  body = bioHub.readBpm();

  Serial.print("Heartrate: ");
  Serial.println(body.heartRate);
  Serial.print("Time between bits: ");
  Serial.println(body.heartRate/60.0);
  Serial.print("Confidence: ");
  Serial.println(body.confidence); 
  Serial.print("Oxygen: ");
  Serial.println(body.oxygen); 
  Serial.print("Status: ");
  Serial.println(body.status);

  lcd->clear();
  lcd->display_message(0, 0, "Ox: "+String(body.oxygen)+"%");
  lcd->display_message(0, 1, "T: "+String(obj_temp)+" F");

  delay(1000);
}