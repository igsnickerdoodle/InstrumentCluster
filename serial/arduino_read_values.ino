#include <ArduinoJson.h>

const byte inPin = 8;

const int numPins = 4;
const int analogInPins[numPins] = {A0, A1};
const int numReadings = 200;
int readings[numPins][numReadings];
int readIndex = 0;
long totals[numPins] = {0, 0};
float averages[numPins] = {0, 0};
const String sensorNames[numPins] = {"Coolant Temp", "Fuel"};

const int mapMaxValues[numPins] = {280, 280};

bool isRunning = false;  // Flag to control whether main loop is executed

void setup() {
  Serial.begin(115200);
  for (int pin = 0; pin < numPins; pin++) {
    for (int i = 0; i < numReadings; i++) {
      readings[pin][i] = 0;
    }
  }
  pinMode(inPin, INPUT);
}

void loop() {
  // Check for start or stop signal from Serial
  while (Serial.available()) {
    String command = Serial.readString();
    if (command.startsWith("START")) {
      isRunning = true;
    }
    if (command.startsWith("STOP")) {
      isRunning = false;
    }
  }

  if (!isRunning) {
    return;  // If isRunning is false, exit the loop
  }

  StaticJsonDocument<200> doc;
  
  for (int pin = 0; pin < numPins; pin++) {
    totals[pin] -= readings[pin][readIndex];

    int analogValue = analogRead(analogInPins[pin]);
    float voltage = analogValue * (5.0 / 1023.0);
    readings[pin][readIndex] = map(voltage * 1000, 0, 5000, 0, mapMaxValues[pin]);

    totals[pin] += readings[pin][readIndex];

    if (sensorNames[pin] != "") {
      doc[sensorNames[pin]] = readings[pin][readIndex];
    }
  }

  readIndex++;

  if (readIndex >= numReadings) {
    readIndex = 0;

    for (int pin = 0; pin < numPins; pin++) {
      averages[pin] = totals[pin] / (float)numReadings;
      averages[pin] = round(averages[pin] * 100) / 100.0;
    }
  }
  
  float RPM;
  if (pulseTime(100000, RPM)) {
    doc["RPM"] = (int)RPM / 2;  // Cast to int to exclude decimals
  }

  serializeJson(doc, Serial);
  Serial.println();
}

boolean pulseTime (unsigned long duration, float& RPM) {
  static int lastInput = digitalRead(inPin);
  static unsigned long start = micros(), lastEventTime = start ; 
  static long count = -1 ; 
  if ((micros() - start) < duration) {           // measure
    if (lastInput != digitalRead(inPin)) {
      lastInput = digitalRead(inPin);
      if (lastInput) {
        lastEventTime = micros();
        count++;
        if (count == 0) start = micros();
      } 
    }
    return false;
  } else {
    if (count == 0 ||  lastEventTime == start) {
      RPM = 0; 
    } else {
      RPM = (6.0E7 * float(count) / float(lastEventTime - start));
    }
    count = -1;
    start = micros();
    return true;
  }   
}
