#include <Servo.h>

Servo thumbServo;
Servo indexServo;
Servo middleServo;
Servo ringServo;
Servo pinkyServo;

void setup() {
  Serial.begin(9600);
  
  thumbServo.attach(13);
  indexServo.attach(12);
  middleServo.attach(11);
  ringServo.attach(10);
  pinkyServo.attach(9);
}

void loop() {
  if (Serial.available() > 0) {
    String servoData = Serial.readStringUntil('\n');
    int angles[5];
    
    int index = 0;
    String angleString = "";
    for (int i = 0; i < servoData.length(); i++) {
      if (servoData[i] == ',') {
        angles[index] = angleString.toInt();
        angleString = "";
        index++;
      } else {
        angleString += servoData[i];
      }
    }
    if (index < 5) {
      angles[index] = angleString.toInt();
    }
    
    thumbServo.write(angles[0]);
    indexServo.write(angles[1]);
    middleServo.write(angles[2]);
    ringServo.write(angles[3]);
    pinkyServo.write(angles[4]);
  }
}
