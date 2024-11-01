void setup() {
  Serial.begin(9600);

  setupRfid();
  setupDHT();
  setupMotors();
  setupServo();
  setupDist();
}


void loop() {
  processRfid();
  processDHT();
  processServo();
  processMotors();

  if (Serial.available() > 0) {
    String data = Serial.readString();

    Serial.println(data);

    if (data.startsWith("servo")) {
      if (data.endsWith("1\n")) {
        servoState = 90;
      } else {
        servoState = 0;
      }
    } else if (data.startsWith("move")) {
      motorsState = true;
    } else if (data.startsWith("tone")) {
      tone(TONE_PIN, 131, 300);
    }
  }
}