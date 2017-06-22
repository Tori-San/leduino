#include <Arduino.h>

int main() {

    init(); // not doing this seems to break delay()
    Serial.begin(115200);
    
    const int LED_PINS[3] = {11, 10, 9}; // B G R
    for (int i = 0; i < 3; ++i) {
        pinMode(LED_PINS[i], OUTPUT);
    }

    uint32_t color = 0xFFFFFF;
    int bytes_read = 0;
    
    const char* HEX_DIGITS = "0123456789ABCDEF";

    while (true) {

        bytes_read = 0;
        
        /* color output
        Serial.print("color: ");
        for (int i = 20; i >= 0; i -= 4) {
            Serial.print(HEX_DIGITS[(color >> i) & 0xF]);
        }
        Serial.println("");
        */

        for (int i = 0; i < 3; ++i) {
            analogWrite(LED_PINS[i], (color >> (8 * i)) & 0xFF);
        }
        
        uint32_t color_buffer = 0;
        
        for (; bytes_read < 3; ++bytes_read) {
            while (!Serial.available()) { /* busy wait */ }
            color_buffer <<= 8;
            color_buffer |= (uint8_t) Serial.read();
        }
        
        color = color_buffer;
    }
}
