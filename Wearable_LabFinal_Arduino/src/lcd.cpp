#include "lcd.h"

LCD::LCD() {
    LCD::lcd = &LiquidCrystal(LCD::rs, LCD::en, LCD::d4, LCD::d5, LCD::d6, LCD::d7);
}

void LCD::setup_lcd() {
    analogWrite(LCD::vo, LCD::contrast);
    LCD::lcd->begin(16, 2);
}

void LCD::display_oxy(float o) {
    LCD::lcd->setCursor(0, 0);
    LCD::lcd->print("Oxygen: ");
    LCD::lcd->print(o);
}

void LCD::display_temp(float t) {
    LCD::lcd->setCursor(0, 1);
    LCD::lcd->print("Temp: ");
    LCD::lcd->print(t);
}

void LCD::clear() {
    LCD::lcd->clear();
}