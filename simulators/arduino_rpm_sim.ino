#include <Encoder.h>

// Requires a rotary knob 

const byte outPin = 9;  // pin for the RPM signal output
const byte encoderPinA = 2;  // pin for encoder signal A
const byte encoderPinB = 3;  // pin for encoder signal B

Encoder myEnc(encoderPinA, encoderPinB);
long oldPosition  = -999;
int RPM = 0;
const int maxRPM = 8000;  // Max RPM value

void setup() {
  pinMode(outPin, OUTPUT);
}

void loop() {
  long newPosition = myEnc.read();
  if (newPosition != oldPosition) {
    oldPosition = newPosition;
    RPM = constrain(newPosition, 0, maxRPM);  // constrain RPM to range 0-maxRPM
  }

  float delayTime = 60000.0 / (2 * RPM);  // Calculate the delay time in microseconds // 2 represents pulses per rotation, each vehicle may be different.
  digitalWrite(outPin, HIGH);  
  delayMicroseconds(delayTime);  
  digitalWrite(outPin, LOW);  
  delayMicroseconds(delayTime);  
}
