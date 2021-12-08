#include <Arduino.h>
#include "lcd.h"
#include "oximeter.h"
#include "thermometer.h"

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

char current_unit;
unsigned long start_time;

void setup()
{
    Serial.begin(115200);
    Wire.begin();

    current_unit = 'F';
    start_time = millis();

    lcd = new LCD(); // It's the same of `lcd = &LCD()`
    lcd->setup_lcd();

    // oximeter = new Oximeter();
    // oximeter->setup();
    // FIXME: OXIMETER hardcoded
    int result = bioHub.begin();
    if (!result)
        Serial.println("Sensor started!");
    else
        Serial.println("Could not communicate with the sensor!!!");

    Serial.println("Configuring Sensor....");
    int error = bioHub.configBpm(MODE_ONE); // Configuring just the BPM settings.
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
    // delay(4000);

    thermometer = new Thermometer();
    if (!thermometer->setup())
    {
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
void lcd_display_values(String ox, String temp, char unit)
{
    lcd->clear();
    lcd->display_message(0, 0, "Oxg:" + ox + "%");
    lcd->display_message(8, 0, "T:" + temp + unit);
}

/**
 * @brief This function calculates if the patient has the fever
 * CDC guidenlines -> Limit of fever CDC -> https://www.cdc.gov/quarantine/maritime/definitions-signs-symptoms-conditions-ill-travelers.html
 *
 * @param temp_C the temperature taken in input is in Celsius.
 */
void display_covid_status(float temp_C)
{
    if (temp_C > 38)
    {
        lcd->display_message(0, 1, "Suggest Cov Test");
    }
    else
    {
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
void display_covid_status(float ox, float temp_C)
{
    if (ox < 95)
    {
        lcd->display_message(0, 3, "Oxg too low");
        delay(1500);
        lcd->display_message(0, 1, "Go to hospital!");
    }
    else if (temp_C > 38)
    {
        lcd->display_message(0, 1, "Suggest Cov Test");
    }
    else
    {
        lcd->display_message(0, 1, "Healthy Patient");
    }
}

float custom_round(float var)
{
    // we use array of chars to store number
    // as a string.
    char str[40];

    // Print in string the value of var
    // with two decimal point
    sprintf(str, "%.1f", var);

    // scan string value in var
    sscanf(str, "%f", &var);

    return var;
}

void loop()
{

    // FIXME: check if thermometer working
    float obj_temp_F = thermometer->getFahrenheitObject();
    float obj_temp_C = thermometer->getCelsiusObject();
    float obj_temp_K = thermometer->getKelvinObject();
    float amb_temp_F = thermometer->getFahrenheitAmbient();
    float amb_temp_C = thermometer->getCelsiusAmbient();
    float amb_temp_K = thermometer->getKelvinAmbient();

    // oximeter->write();
    // FIXME: OXIMETER hardcoded
    body = bioHub.readBpm();
    uint8_t oxim_status = body.status;
    uint8_t oxygen = body.oxygen;

    if (millis() - start_time > 5000)
    {
        if (current_unit == 'F')
            current_unit = 'C';
        else
            current_unit = 'F';

        start_time = millis();
    }

    // FIXME: the temperature in Fahrenheit must be with only one decimal digit if it is over 100
    if (oxim_status == uint8_t(OximeterStatus::NO_OBJ))
    {
        String temp_to_display;
        if (current_unit == 'F')
        {
            // Useful for displaying only 4 total digits
            temp_to_display = obj_temp_F > 100 ? String(int(obj_temp_F)) : String(obj_temp_F);
        }
        else
        {
            temp_to_display = String(obj_temp_C);
        }
        lcd_display_values("N/A", temp_to_display, current_unit);
        display_covid_status(obj_temp_C);
    }
    else if (oxim_status != uint8_t(OximeterStatus::FING_DET))
    {
        if (current_unit == 'F')
            lcd_display_values("N/A", obj_temp_F > 100 ? String(int(obj_temp_F)) : String(obj_temp_F), current_unit);
        else
            lcd_display_values("N/A", String(obj_temp_C), current_unit);

        lcd->display_message(0, 1, "Measuring Oxg..");
    }
    else if (oxim_status == uint8_t(OximeterStatus::FING_DET))
    {
        String temp_to_display;
        if (current_unit == 'F')
        {
            temp_to_display = obj_temp_F > 100 ? String(int(obj_temp_F)) : String(obj_temp_F);
        }
        else
        {
            temp_to_display = String(obj_temp_C);
        }
        lcd_display_values(String(oxygen), temp_to_display, current_unit);
        display_covid_status(oxygen, obj_temp_C);
    }

    Serial.print(obj_temp_F);
    Serial.print("+");
    Serial.print(obj_temp_C);
    Serial.print("+");
    Serial.print(obj_temp_K);
    Serial.print("+");
    Serial.print(amb_temp_F);
    Serial.print("+");
    Serial.print(amb_temp_C);
    Serial.print("+");
    Serial.print(amb_temp_K);
    Serial.print("+");
    Serial.print(body.status);
    Serial.print("+");
    Serial.print(body.oxygen);
    Serial.print("+");
    Serial.print(body.confidence);
    Serial.print("+");
    Serial.print(body.heartRate);
    Serial.print("+");
    Serial.println(" ");

    delay(100);
}