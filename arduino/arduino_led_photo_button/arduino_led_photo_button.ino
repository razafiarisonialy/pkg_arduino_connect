const int PIN_ROUGE = 9;
const int PIN_BLEU  = 10;
const int PIN_VERT  = 8;
const int boutonPin = 2; 
volatile bool isInterrupt = false;  
const int photoPin = A0;
int photoval = 0;

void eteindreTout() {
  digitalWrite(PIN_ROUGE, HIGH);
  digitalWrite(PIN_VERT, HIGH);
  digitalWrite(PIN_BLEU, HIGH);
}

void setCouleur(bool rouge, bool vert, bool bleu) {
  digitalWrite(PIN_ROUGE, rouge ? LOW : HIGH);
  digitalWrite(PIN_VERT,  vert  ? LOW : HIGH);
  digitalWrite(PIN_BLEU,  bleu  ? LOW : HIGH);
}

void setup() {
  Serial.begin(115200);

  pinMode(PIN_ROUGE, OUTPUT);
  pinMode(PIN_VERT, OUTPUT);
  pinMode(PIN_BLEU, OUTPUT);
  pinMode(boutonPin, INPUT);

  attachInterrupt(
    digitalPinToInterrupt(boutonPin),
    interrupt,                 
    CHANGE                          
  );

  eteindreTout();

}

void interrupt() {
  if (digitalRead(boutonPin) == HIGH) {
    isInterrupt = !isInterrupt;
  }
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "ROUGE")      setCouleur(true, false, false);
    else if (command == "VERT")  setCouleur(false, true, false);
    else if (command == "BLEU")  setCouleur(false, false, true);
    else if (command == "JAUNE") setCouleur(true, true, false);
    else if (command == "CYAN")  setCouleur(false, true, true);
    else if (command == "MAGENTA") setCouleur(true, false, true);
    else if (command == "BLANC") setCouleur(true, true, true);
    else eteindreTout();
  }

  photoval = map(analogRead(photoPin), 0, 1023, 0, 255);


  Serial.print("{\"photoResistor\": ");
  Serial.print(photoval);
  Serial.print(", \"bouton\": ");
  Serial.print(isInterrupt ? "true" : "false");
  Serial.println("}");
  delay(200);
}