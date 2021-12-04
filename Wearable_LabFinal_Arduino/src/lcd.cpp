#include "lcd.h"

LCD::LCD() {
    LCD::lcd =  new LiquidCrystal(LCD::rs, LCD::en, LCD::d4, LCD::d5, LCD::d6, LCD::d7);
}

void LCD::setup_lcd() {
    analogWrite(LCD::vo, LCD::contrast);
    LCD::lcd->begin(16, 2);
}

void LCD::display_message(int x, int y, String message) {
    LCD::lcd->setCursor(x, y);
    LCD::lcd->print(message);
}

void LCD::clear() {
    LCD::lcd->clear();
}

void LCD::display_error(String error) {
    LCD::lcd->clear();
    LCD::lcd->setCursor(0,0);
    LCD::lcd->print(error);
}