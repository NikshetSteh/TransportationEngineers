void setupRfid() {
  SPI.begin();
  rfid.PCD_Init();
  rfid.PCD_SetAntennaGain(rfid.RxGain_max);
  rfid.PCD_AntennaOff();
  rfid.PCD_AntennaOn();

  for (byte i = 0; i < 6; i++) {  // Default key
    rfid_key.keyByte[i] = 0xFF;
  }
}

void processRfid() {
  static uint32_t rebootTimer = millis();  // Важный костыль против зависания модуля!
  if (millis() - rebootTimer >= 1000) {    // Таймер с периодом 1000 мс
    rebootTimer = millis();                // Обновляем таймер
    digitalWrite(RFID_RST_PIN, HIGH);      // Сбрасываем модуль
    delayMicroseconds(2);                  // Ждем 2 мкс
    digitalWrite(RFID_RST_PIN, LOW);       // Отпускаем сброс
    rfid.PCD_Init();                       // Инициализируем заного
  }
  if (!rfid.PICC_IsNewCardPresent()) return;  // Если новая метка не поднесена - вернуться в начало loop
  if (!rfid.PICC_ReadCardSerial()) return;    // Если метка не читается - вернуться в начало loop
  if (millis() - rfidTimout < 1000) {
    return;
  }

  rfidTimout = millis();
  Serial.print("key ");
  for (uint8_t i = 0; i < 4; i++) {          // Цикл на 4 итерации
    Serial.print("0x");                      // В формате HEX
    Serial.print(rfid.uid.uidByte[i], HEX);  // Выводим UID по байтам
    Serial.print(" ");
  }
  Serial.println("");
}





void setupDHT() {
  dht.begin();
}

void processDHT() {
  if (millis() - telemetryTimer < TELEMETRY_TIMER) {
    return;
  }

  telemetryTimer = millis();

  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println("!telemetry failed");
    return;
  }
  Serial.print("telemetry ");
  Serial.print(h);
  Serial.print(" ");
  Serial.println(t);
  /*Serial.print(t);
  Serial.print(" ");
  Serial.println(getDist());*/
}





void setupServo() {
  servo1.attach(SERVO_1_PIN);
}

void processServo() {
  servo1.write(servoState);
}





void setupMotors() {
  pinMode(MOTOR_LEFT_F_PIN, OUTPUT);
  pinMode(MOTOR_LEFT_B_PIN, OUTPUT);
  pinMode(MOTOR_RIGHT_F_PIN, OUTPUT);
  pinMode(MOTOR_RIGHT_B_PIN, OUTPUT);

  pinMode(MOTOR_SPEED_PIN, OUTPUT);
}

void processMotors() {
  if (!motorsState) {
    return;
  }

  if (getDist() <= 5) {
    tone(TONE_PIN, 131, 300);

    digitalWrite(MOTOR_LEFT_F_PIN, 0);
    digitalWrite(MOTOR_LEFT_B_PIN, 0);
    digitalWrite(MOTOR_RIGHT_F_PIN, 0);
    digitalWrite(MOTOR_RIGHT_B_PIN, 0);

    return;
  }

  analogWrite(MOTOR_SPEED_PIN, 110);

  if ((analogRead(S_LEFT_PIN) < 500) && (analogRead(S_RIGHT_PIN) < 500)) {
    digitalWrite(MOTOR_LEFT_F_PIN, 1);
    digitalWrite(MOTOR_LEFT_B_PIN, 0);
    digitalWrite(MOTOR_RIGHT_F_PIN, 1);
    digitalWrite(MOTOR_RIGHT_B_PIN, 0);
    motorsTimeoutStarted = false;
  } else if ((analogRead(S_LEFT_PIN) <= 500) && (analogRead(S_RIGHT_PIN) > 500)) {
    digitalWrite(MOTOR_LEFT_F_PIN, 0);
    digitalWrite(MOTOR_LEFT_B_PIN, 0);
    digitalWrite(MOTOR_RIGHT_F_PIN, 1);
    digitalWrite(MOTOR_RIGHT_B_PIN, 0);
    motorsTimeoutStarted = false;
  } else if ((analogRead(S_LEFT_PIN) > 500) && (analogRead(S_RIGHT_PIN) <= 500)) {
    digitalWrite(MOTOR_LEFT_F_PIN, 1);
    digitalWrite(MOTOR_LEFT_B_PIN, 0);
    digitalWrite(MOTOR_RIGHT_F_PIN, 0);
    digitalWrite(MOTOR_RIGHT_B_PIN, 0);
    motorsTimeoutStarted = false;
  } else {
    if (motorsTimeoutStarted && millis() - motorsTimeout > 400) {
      motorsState = false;
    }

    motorsTimeout = millis();
    motorsTimeoutStarted = true;
    digitalWrite(MOTOR_LEFT_F_PIN, 0);
    digitalWrite(MOTOR_LEFT_B_PIN, 0);
    digitalWrite(MOTOR_RIGHT_F_PIN, 0);
    digitalWrite(MOTOR_RIGHT_B_PIN, 0);
  }
}





void setupDist() {
  pinMode(DIST_TRIG_PIN, OUTPUT);
  pinMode(DIST_ECHO_PIN, INPUT);
}

int getDist() {
  int duration, cm;
  digitalWrite(DIST_TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(DIST_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(DIST_TRIG_PIN, LOW);
  duration = pulseIn(DIST_ECHO_PIN, HIGH);
  cm = duration / 58;
  return cm;
}