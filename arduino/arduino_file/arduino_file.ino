const int PIN_ROUGE = 9;
const int PIN_VERT  = 10;
const int PIN_BLEU  = 11;

void eteindreTout() {
  digitalWrite(PIN_ROUGE, LOW);
  digitalWrite(PIN_VERT, LOW);
  digitalWrite(PIN_BLEU, LOW);
}

void setCouleur(bool rouge, bool vert, bool bleu) {
  digitalWrite(PIN_ROUGE, rouge ? HIGH : LOW);
  digitalWrite(PIN_VERT,  vert  ? HIGH : LOW);
  digitalWrite(PIN_BLEU,  bleu  ? HIGH : LOW);
}

void setup() {
  Serial.begin(115200);

  pinMode(PIN_ROUGE, OUTPUT);
  pinMode(PIN_VERT, OUTPUT);
  pinMode(PIN_BLEU, OUTPUT);

  eteindreTout();
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
}