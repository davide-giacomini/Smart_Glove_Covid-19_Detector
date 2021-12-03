#include <Arduino.h>
// #include <LiquidCrystal.h>
// #include <Wire.h>
// #include "lcd.h"

// const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2, vo = 6, contrast = 75;
// LiquidCrystal lcd = LiquidCrystal(rs, en, d4, d5, d6, d7);

// void setup_lcd() {
//   analogWrite(vo, contrast);
//   lcd.begin(16, 2);
//   Serial.begin(115200);
// }

// void setup() {
//   setup_lcd();

// }

// int readOxy() {
//   int o = 68; // TODO check oximeter read
//   return o;
// }

// float readTemp() {
//   float t = 93; // TODO check temp read
//   return t;
// }

// float readHB() {
//   float hb = 57; // TODO check heartbeat read
//   return hb;
// }

// void sendOxy(int o) { // TODO send data function send everything in one function
//   Serial.print(o);
// }

// void sendTemp(float t) {
//   Serial.print("+");
//   Serial.print(t);
// }

// void sendHB(float hb) {
//   Serial.print("+");
//   Serial.println(hb);
// }

// void displayOxy(int o) {
//   lcd.setCursor(0, 0);
//   lcd.print("Oxygen: ");
//   lcd.print(o);
// }

// void displayTemp(float t) {
//   lcd.setCursor(0, 1);
//   lcd.print("Temp: ");
//   lcd.print(t); 
// }

// void loop() {

//   int oxy = readOxy();
//   float temp = readTemp();
//   float heartbeat = readHB();

//   sendOxy(oxy);
//   sendTemp(temp);
//   sendHB(heartbeat);

//   lcd.clear();
  
//   displayOxy(oxy);
//   displayTemp(temp);

//   delay(250);
// }


// SKETCH FOR TESTING I2C
/////////////
// #include <Wire.h>

// int address_sensor1= 72; //binary equivalent is 1001000

// int address_sensor2= 73; //binary equivalent is 1001001

// void setup(){

// Serial.begin(9600); //this creates the Serial Monitor
// Wire.begin(); //this creates a Wire object
// }

// void loop(){
// Wire.beginTransmission(address_sensor1); //Send a request to begin communication with the device at the specified address

// Wire.write(0); //Sends a bit asking for register 0, the data register of the TC74 sensor

// Wire.endTransmission(); //this ends transmission of data from the arduino to the temperature sensor

// //this now reads the temperature from the TC74 sensor
// Wire.requestFrom(address_sensor1, 1);//this requests 1 byte from the specified address

// while(Wire.available() == 0);
// int celsius1= Wire.read();

// int fahrenheit1= round(celsius1 * 9.0/5.0 + 32.0);

// Serial.print("Temperature sensor 1:");
// Serial.print(celsius1);
// Serial.print("degrees celsius ");
// Serial.print(fahrenheit1);
// Serial.print(" degrees Fahrenheit");

// delay(2000);
// Wire.beginTransmission(address_sensor2); //Send a request to begin communication with the device at the specified address

// Wire.write(0); //Sends a bit asking for register 0, the data register of the TC74 sensor

// Wire.endTransmission(); //this ends transmission of data from the arduino to the temperature sensor

// //this now reads the temperature from the TC74 sensor
// Wire.requestFrom(address_sensor2, 1);//this requests 1 byte from the specified address

// while(Wire.available() == 0);
// int celsius2= Wire.read();

// int fahrenheit2= round(celsius2 * 9.0/5.0 + 32.0);

// Serial.print("Temperature sensor 2:"); Serial.print(celsius2);
// Serial.print("degrees celsius ");
// Serial.print(fahrenheit2);
// Serial.print(" degrees Fahrenheit");

// delay(2000);
// }


// SCANNER SKETCH
// #include <Wire.h> //include Wire.h library

// void setup()
// {
//   Wire.begin(); // Wire communication begin
//   Serial.begin(115200); // The baudrate of Serial monitor is set in 9600
//   while (!Serial); // Waiting for Serial Monitor
//   Serial.println("\nI2C Scanner");
// }

// void loop()
// {
//   byte error, address; //variable for error and I2C address
//   int nDevices;

//   Serial.println("Scanning...");

//   nDevices = 0;
//   for (address = 1; address < 127; address++ )
//   {
//     // The i2c_scanner uses the return value of
//     // the Write.endTransmisstion to see if
//     // a device did acknowledge to the address.
//     Wire.beginTransmission(address);
//     error = Wire.endTransmission();

//     if (error == 0)
//     {
//       Serial.print("I2C device found at address 0x");
//       if (address < 16)
//         Serial.print("0");
//       Serial.print(address, HEX);
//       Serial.println("  !");
//       nDevices++;
//     }
//     else if (error == 4)
//     {
//       Serial.print("Unknown error at address 0x");
//       if (address < 16)
//         Serial.print("0");
//       Serial.println(address, HEX);
//     }
//   }
//   if (nDevices == 0)
//     Serial.println("No I2C devices found\n");
//   else
//     Serial.println("done\n");

//   delay(5000);
// }





//////////////////////////////
// LAB1 OXIMETER

#include <SparkFun_Bio_Sensor_Hub_Library.h>
#include <Wire.h>

// No other Address options.
#define DEF_ADDR 0x55

// Reset pin, MFIO pin
const int resPin = 4;
const int mfioPin = 5;

// Takes address, reset pin, and MFIO pin.
SparkFun_Bio_Sensor_Hub bioHub(resPin, mfioPin); 

#define USER_AGE 23
#define MAX_HR 220-23

bioData body;

long timeCount = 0.0;
unsigned long real_time;
float bpm = 0.0;
bool bpmCheck = false;
int bpms[30];

float heart_rate;
float time_btw_beats;
float blood_oxyg;
unsigned short confidence_level;


void setup(){

  Serial.begin(115200);

  Wire.begin();
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
  delay(4000); 

}

/*enum class Status : uint8_t {
   NO_OBJECT_DETECTED = 0,
   OBJECT_DETECTED = 1,
   OBJECT_OTHER_THAN_FINGER_DETECTED = 2,
   FINGER_DETECTED = 3
};

Status get_enum_from_value(uint8_t value) {
  
  switch (value):
     case 0:
      return NO_OBJECT_DETECTED;
      break;
     case 1:
      return OBJECT_DETECTED;
      break;
     case 2:
      return OBJECT_OTHER_THAN_FINGER_DETECTED;
      break;
     case 3:
      return FINGER_DETECTED;
      break;
}

Status status;*/

void loop(){

    // Information from the readBpm function will be saved to our "body"
    // variable.  
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
    
    if (!bpmCheck) {
      if (timeCount < 30) {

        float currentBpm = body.heartRate;

        if (currentBpm!=0) {
          
          bpms[timeCount] = currentBpm;
          Serial.print("timeCount = ");
          Serial.println(timeCount);
  
          if (timeCount == 29) {
            Serial.println("ENTERING THE AVERAGE PHASE");
            long sum = 0;
              for (int i = 0; i < 30; i++) {
                sum = sum + bpms[i];
              }
            bpm = sum / 30.0;
            Serial.print("bpm = ");
            Serial.println(bpm);
            bpmCheck = true;
          }
          
          timeCount++;
        }
      }
    }
    
    delay(1000); // Slowing it down, we don't need to break our necks here.
}


// EXAMPLE THERMOMETER

// #include <Wire.h> // I2C library, required for MLX90614
// #include <SparkFunMLX90614.h> //Click here to get the library: http://librarymanager/All#Qwiic_IR_Thermometer by SparkFun

// IRTherm therm; // Create an IRTherm object to interact with throughout

// void setup() 
// {
//   Serial.begin(115200); // Initialize Serial to log output
//   Wire.begin(); //Joing I2C bus
  
//   if (therm.begin() == false){ // Initialize thermal IR sensor
//     Serial.println("Qwiic IR thermometer did not acknowledge! Freezing!");
//     while(1);
//   }
//   Serial.println("Qwiic IR Thermometer did acknowledge.");
  
//   therm.setUnit(TEMP_F); // Set the library's units to Farenheit
//   // Alternatively, TEMP_F can be replaced with TEMP_C for Celsius or
//   // TEMP_K for Kelvin.
  
//   pinMode(LED_BUILTIN, OUTPUT); // LED pin as output
// }

// void loop() 
// {
//   digitalWrite(LED_BUILTIN, HIGH);
    
//   // Call therm.read() to read object and ambient temperatures from the sensor.
//   if (therm.read()) // On success, read() will return 1, on fail 0.
//   {
//     // Use the object() and ambient() functions to grab the object and ambient
// 	// temperatures.
// 	// They'll be floats, calculated out to the unit you set with setUnit().
//     Serial.print("Object: " + String(therm.object(), 2));
//     Serial.println("F");
//     Serial.print("Ambient: " + String(therm.ambient(), 2));
//     Serial.println("F");
//     Serial.println();
//   }
//   digitalWrite(LED_BUILTIN, LOW);
//   delay(1000);
// }



// LCD EXAMPLE

// #include <Arduino.h>
// #include <LiquidCrystal.h>
// #include <Wire.h>

// const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2, vo = 6, contrast = 75;
// LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// void setup() {
//   lcd.begin(16, 2);
//   Serial.begin(115200);
// }

// void displayOxy(int o) {
//   lcd.setCursor(0, 0);
//   lcd.print("Oxygen: ");
//   lcd.print(o);
// }

// void displayTemp(float t) {
//   lcd.setCursor(0, 1);
//   lcd.print("Temp: ");
//   lcd.print(t);
// }

// int count = 0;
// void loop() {
//   int oxy = 98;
//   float temp = 57;

//   lcd.clear();

//   displayOxy(oxy+count);
//   displayTemp(temp+count);
//   delay(500);
//   count++;
// }