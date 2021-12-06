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

/**
 * @brief It displays the temperature and the oxygen level on the LCD.
 * 
 * @param ox it must be a string
 * @param temp it must be a string
 * @param unit it must be a char either 'F', 'C', 'K'.
 */
void lcd_display_f(String ox, String temp, char unit) {
    lcd->clear();
    lcd->display_message(0, 0, "Oxg:"+ ox +"%");
    lcd->display_message(8, 0, "T:"+ temp + unit);
}

/**
 * @brief This function calculates if the patient has the fever 
 * CDC guidenlines -> Limit of fever CDC -> https://www.cdc.gov/quarantine/maritime/definitions-signs-symptoms-conditions-ill-travelers.html
 * 
 * @param temp_C the temperature taken in input is in Celsius.
 */
void display_covid_status(float temp_C) {
  if (temp_C > 38) {
    lcd->display_message(0, 1, "Suggest Cov Test");
  }
  else {
    lcd->display_message(0, 1, "Healthy Patient");
  }
}

/**
 * @brief This function calculates if the patient has the fever 
 * CDC guidenlines:
 * - Limit of fever CDC -> https://www.cdc.gov/quarantine/maritime/definitions-signs-symptoms-conditions-ill-travelers.html
 * - Limit of oxygen saturation CDC -> https://www.cdc.gov/coronavirus/2019-ncov/videos/oxygen-therapy/Basics_of_Oxygen_Monitoring_and_Oxygen_Therapy_Transcript.pdf
 * 
 * @param ox this is the oxygen in percentage
 * @param temp_C the temperature taken in input is in Celsius.
 */
void display_covid_status(float ox, float temp_C) {
  if (ox < 95) {
    lcd->display_message(0, 1, "Oxg too low. Go to the hospital!");
  }
  else if (temp_C > 38) {
    lcd->display_message(0, 1, "Suggest Cov Test");
  }
  else {
    lcd->display_message(0, 1, "Healthy Patient");
  }
}

void loop() {

  // FIXME: check if thermometer working
  float obj_temp_F = thermometer->getFahrenheitObject();
  float obj_temp_C = thermometer->getCelsiusObject();
  float obj_temp_K = thermometer->getKelvinObject();
  float amb_temp_F = thermometer->getFahrenheitAmbient();
  float amb_temp_C = thermometer->getCelsiusAmbient();
  float amb_temp_K = thermometer->getKelvinAmbient();

  // oximeter->write();
  //FIXME: OXIMETER hardcoded
  body = bioHub.readBpm();
  uint8_t oxim_status = body.status;
  uint8_t oxygen = body.oxygen;

  if (oxim_status == uint8_t(OximeterStatus::NO_OBJ)) {
    lcd_display_f("N/A", String(obj_temp_F), 'F');
    display_covid_status(obj_temp_C);
  }
  else if (oxim_status != uint8_t(OximeterStatus::FING_DET)) {
    lcd_display_f("N/A", String(obj_temp_F), 'F');
    lcd->display_message(0, 1, "Measuring Oxg..");
  }
  else if (oxim_status == uint8_t(OximeterStatus::FING_DET)) {
    lcd_display_f(String(oxygen), String(obj_temp_F), 'F');
    display_covid_status(oxygen, obj_temp_C);
  }

  // Serial.print("Heartrate: ");
  // Serial.println(body.heartRate);
  // Serial.print("Time between bits: ");
  // Serial.println(body.heartRate/60.0);
  // Serial.print("Confidence: ");
  // Serial.println(body.confidence); 
  // Serial.print("Oxygen: ");
  // Serial.println(body.oxygen); 
  // Serial.print("Status: ");
  // Serial.println(body.status);

  // lcd->clear();
  // lcd->display_message(0, 0, "Oxg:"+String(body.oxygen)+"%");
  // lcd->display_message(8, 0, "T:"+String(obj_temp_F)+"F");
  // lcd->display_message(0, 1, "Suggest Cov test");

  delay(1000);
}