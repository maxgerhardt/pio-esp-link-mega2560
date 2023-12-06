#include <Arduino.h>
#define LED LED_BUILTIN
void setup() {
    pinMode(LED, OUTPUT);
    Serial.begin(115200);
}

void loop() {
    digitalWrite(LED, HIGH);    
    delay(500);
    digitalWrite(LED, LOW);
    delay(500);
    Serial.println("Blinky from Mega!");
}