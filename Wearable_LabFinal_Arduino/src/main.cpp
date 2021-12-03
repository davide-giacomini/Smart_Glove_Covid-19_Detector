#include <Arduino.h>
#include <LiquidCrystal.h>
#include <Wire.h>
#include "lcd.h"
#include "oximeter.h"

#define USER_AGE 23
#define MAX_HR 220-23

// WARNING: I initially did `LCD lcd()`, but it doesn't work because the compiler messes something up with the order of constructors call. The issue and solutions are well documented here: https://arduino.stackexchange.com/questions/23168/library-liquidcrystal-i2c-dont-work-in-other-class-composition/23240
LCD *lcd;

void setup() {
  lcd = new LCD(); // It's the same of `lcd = &LCD()`
  lcd->setup_lcd();
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

  int oxy = readOxy();
  float temp = readTemp();
  float heartbeat = readHB();

  sendOxy(oxy);
  sendTemp(temp);
  sendHB(heartbeat);

  lcd->clear();
  lcd->display_oxy(oxy);
  lcd->display_temp(temp);

  delay(1000);
}