#include <Arduino.h>
#include <LiquidCrystal.h>

class LCD {
public:
    static const int rs = 12;    // Reset pin
    static const int en = 11;    // Enable pin
    static const int d4 = 5;
    static const int d5 = 4;
    static const int d6 = 3;
    static const int d7 = 2;
    static const int vo = 6;
    static const int contrast = 75;

    LCD();
    void setup_lcd();
    void display_oxy(int o);
    void display_temp(float t);
    void clear();
private:
    LiquidCrystal *lcd;
};