#include <Arduino.h>
#include <LiquidCrystal.h>

/**
 * @brief The LCD object is useful to encapsulate all the information of the LCD sensor
 * We are using an LCD screen 16x2 (https://www.amazon.com/HiLetgo-Display-Backlight-Controller-Character/dp/B00HJ6AFW6/ref=sr_1_3?keywords=lcd+screen+16x2&qid=1639352794&sr=8-3)
 * 
 */
class LCD {
public:
    static const int rs = 12;    // Reset pin
    static const int en = 11;    // Enable pin
    // d* are the LCD pins, and the numbers are the 
    static const int d4 = 5;
    static const int d5 = 4;
    static const int d6 = 3;
    static const int d7 = 2;
    static const int vo = 6;
    static const int contrast = 75;

    LCD();
    void setup_lcd();
    void clear();
    void display_error(String error);
    /**
     * @brief Display the message starting from the position indicated
     * 
     * @param x x position
     * @param y y position
     * @param message the message to display
     */
    void display_message(int x, int y, String message);
private:
    /**
     * @brief This is a reference to the Arduino object LiquidCrystal
     * 
     */
    LiquidCrystal *lcd;
};