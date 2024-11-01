MFRC522 rfid(RFID_SS_PIN, RFID_RST_PIN);  
MFRC522::MIFARE_Key rfid_key;        
MFRC522::StatusCode rfid_status;

DHT dht(DHT_PIN, DHT11);

Servo servo1;

unsigned long rfidTimout = 0;
unsigned long telemetryTimer = 0;

byte servoState;

boolean motorsState = false;
unsigned long motorsTimeout = 0;
bool motorsTimeoutStarted = false;
