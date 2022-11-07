String inputString = "";
bool stringComplete = false;

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

void setup() {
  Serial.begin(9600);
  inputString.reserve(200);
}

void loop() {
  if (stringComplete) {
    bool sentH=false, correct=true;
    int stepInt=0;
    String stepStr="";
    String command=inputString;
    if(command[0] == '+'){
      sentH=true; Serial.println("HORARIO");
    }
    else if(command[0] == '-'){
      sentH=false; Serial.println("Anti-HORARIO");
    }
    else{correct=false;}

    if(correct==true){
      for(int i=1; i<command.length(); i++){
        stepStr+=command[i];
      }
      stepInt = stepStr.toInt();
      Serial.println(stepInt);
    }
    
    inputString = "";
    stringComplete = false;
  }
}