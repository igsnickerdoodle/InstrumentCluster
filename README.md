## Python Based Project for Initializing Instrument Cluster on RaspberryPi


Project entails utilizing containers, python, raspberry pi, and arduinos. 

Arduinos connect via USB into the raspberry pi, and then are passed into the containers that are deployed to run the application.

---
# Implementation and Integration
**Required Items**
- Raspberry Pi 4/5 8G
- LCD Screen
- Arduino Uno or Nano
- Resistors *(Refer to the Voltage Divider section)*
- Diodes

---
# Current Problems
 - Raspberry Pi start up times need improvement
 - Dynamic scaling needs to be incorporated into current designs





 ## Arduino ##
 Connecting Analog Vehicle Inputs into Arduino

 11-15v stablization requires utilizing resistors.
 

### Voltage Divider Combinations to Get ~5V from 14.7V

1. **12kΩ and 6.8kΩ**
   - **R1:** 12kΩ
   - **R2:** 6.8kΩ
   - **Output Voltage:** `14.7V * (6.8kΩ / (12kΩ + 6.8kΩ)) ≈ 5.12V`

2. **18kΩ and 10kΩ**
   - **R1:** 18kΩ
   - **R2:** 10kΩ
   - **Output Voltage:** `14.7V * (10kΩ / (18kΩ + 10kΩ)) ≈ 5.03V`

3. **33kΩ and 18.5kΩ**
   - **R1:** 33kΩ
   - **R2:** 18.5kΩ
   - **Output Voltage:** `14.7V * (18.5kΩ / (33kΩ + 18.5kΩ)) ≈ 5.00V`

4. **22kΩ and 12.4kΩ**
   - **R1:** 22kΩ
   - **R2:** 12.4kΩ
   - **Output Voltage:** `14.7V * (12.4kΩ / (22kΩ + 12.4kΩ)) ≈ 5.00V`

5. **47kΩ and 26.4kΩ**
   - **R1:** 47kΩ
   - **R2:** 26.4kΩ
   - **Output Voltage:** `14.7V * (26.4kΩ / (47kΩ + 26.4kΩ)) ≈ 5.05V`
 
### Serialized Inputs Signals

| Reference | Arduino Uno Pin | On | Off |
|:---------:|:-----------:|:--:|:---:|
|Engine RPM|
|Speed|
|Coolant Temp|
|Coolant Warning|
|Oil Temp|
|Low Oil|
|Oil Pressure|
|Fuel Level|
|Low Fuel|
|CEL|
|ABS|
|Seatbelt|
|Boost Gauge|
|AFR|

*This is what I used for reference in my application. Tailor it to your specific needs.*