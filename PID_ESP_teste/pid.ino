int RST = D8, SLP = D1,  ENA = D7, MS1 = D4, MS2 = D5, MS3 = D6, DIR = D3, STP = D2;
int MeioPeriodo = 3000;
bool somaSubDaRef=false;
int referencia=0;
int limitePassos=300;

int vazaoMax=55, vazaoMin=0;

int counter = 0;
unsigned long timePassed=0;
String inputString = "";
bool stringComplete = false;

double erroAtual, somatorioErro=0, ganhoKp, ganhoKi;
int Setpoint, Input, Output;
double Kp=0.6, Ki=0.3;

const int sensor=10;
int intOut, oldOut, diferenca;

IRAM_ATTR void SensorCctivated(){
  counter++;
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

void CalculaPID(){
  Input=counter;
  erroAtual = Setpoint-Input;
  somatorioErro+=erroAtual;
  ganhoKp=erroAtual*Kp;
  ganhoKi=somatorioErro*Ki;
  if((Setpoint>Input)&&(referencia>0)){
    Output=abs(ganhoKp+ganhoKi);
  }else if((Setpoint < Input)&&(referencia<limitePassos)){
    Output=abs(ganhoKp+ganhoKi);
  }
  
}

void setup() {
  Serial.begin(57600);
  inputString.reserve(200);
  pinMode(sensor, INPUT);
  attachInterrupt(digitalPinToInterrupt(sensor), SensorCctivated, RISING);
  Setpoint=30;
  pinMode(SLP, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(MS3, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(STP, OUTPUT);
  pinMode(RST, OUTPUT);
  digitalWrite(SLP, HIGH);
  disa_A4988();
  rst_A4988();
  AHR();
  TesteMotor(limitePassos);
}

void loop() {
  if(millis() - timePassed >= 1000){
    timePassed = millis();
    CalculaPID();
    Serial.print(Setpoint);
    Serial.print(" ");
    Serial.println(Input);
    //Serial.print("Set: ");
    //Serial.print(Setpoint);
    //Serial.print("; Input: ");
    //Serial.print(Input);
    //Serial.print("; Output: ");
    //Serial.print(Output);
    //Serial.print("; OldOutput: ");
    //Serial.print(oldOut);
    if(Setpoint == Input){
      //Serial.print("; Parado");
    }else{
      if((Setpoint > Input)&&(referencia>0)){
        AHR(); //abre
        somaSubDaRef=false; //subtrai
        //Serial.print("; Abre");
      }else if((Setpoint < Input)&&(referencia<limitePassos)){
        HOR(); //fecha
        somaSubDaRef=true; //soma
        //Serial.print("; Fecha");
      }
      int passos=map(Output,0,vazaoMax,0,limitePassos);
      //Serial.print("; Passos: ");
      //Serial.print(passos);
      if(passos > 0){
        if((somaSubDaRef == false)&&(passos>referencia)){
          passos=referencia;
        }else if((somaSubDaRef == true)&&(passos>(limitePassos-referencia))){
          passos=limitePassos-referencia;
        }
        TesteMotor(passos);
      }
      if((somaSubDaRef == false)&&(referencia>0)){
        referencia-=passos;
      }else if((somaSubDaRef == true)&&(referencia<limitePassos)){
        referencia+=passos;
      }
      
    }
    //Serial.print("; bool: ");
    //Serial.print(somaSubDaRef);
    //Serial.print("; Ref: ");
    //Serial.println(referencia);
    oldOut=intOut;
    counter=0;
  }
  if (stringComplete){
    int valueInt=0;
    String valueStr="";
    String command="";
    Setpoint=inputString.toInt();
    
    
    inputString = "";
    stringComplete = false;
  }
}