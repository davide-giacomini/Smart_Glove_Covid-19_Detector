#include <Arduino.h>
#include <LiquidCrystal.h>

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2, vo = 6, contrast = 75;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  analogWrite(vo, contrast);
  lcd.begin(16, 2);
  Serial.begin(115200);

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

void displayOxy(int o) {
  lcd.setCursor(0, 0);
  lcd.print("Oxygen: ");
  lcd.print(o);
}

void displayTemp(float t) {
  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
  lcd.print(t); 
}

void loop() {

  int oxy = readOxy();
  float temp = readTemp();
  float heartbeat = readHB();

  sendOxy(oxy);
  sendTemp(temp);
  sendHB(heartbeat);

  lcd.clear();
  
  displayOxy(oxy);
  displayTemp(temp);

  delay(250);
}
