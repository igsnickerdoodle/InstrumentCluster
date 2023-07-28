const byte inPin = 8;
float RPM = 0; 

void setup() {
  pinMode(inPin, INPUT);
  Serial.begin(115200);
}

void loop() {
  if (pulseTime(100000)) {
    Serial.print("RPM: ");
    Serial.println((int)RPM / 2);  // Cast to int to exclude decimals
  }
}

boolean pulseTime (unsigned long duration) {
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
