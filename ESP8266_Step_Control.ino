int RST = D8;              // Porta digital D08 - reset do A4988
int SLP = D1;              // Porta digital D09 - dormir (sleep) A4988
int ENA = D7;              // Porta digital D07 - ativa (enable) A4988
int MS1 = D4;              // Porta digital D04 - MS1 do A4988
int MS2 = D5;              // Porta digital D05 - MS2 do A4988
int MS3 = D6;              // Porta digital D06 - MS3 do A4988
int DIR = D3;              // Porta digital D03 - direção (direction) do A4988
int STP = D2;              // Porta digital D02 - passo(step) do A4988

int MeioPeriodo = 3000;
bool cont = true;

void setup()
{
  Serial.begin(9600);
  
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
}

void rst_A4988()
{
  digitalWrite(RST, LOW);
  //delay (10);
  digitalWrite(RST, HIGH);
  //delay (10);
}

void disa_A4988(){digitalWrite(ENA, HIGH);}
void ena_A4988(){digitalWrite(ENA, LOW);}
void HOR(){digitalWrite(DIR, HIGH);}
void AHR(){digitalWrite(DIR, LOW);}

void PASSO(){
  digitalWrite(STP, LOW);
  delayMicroseconds (MeioPeriodo);
  digitalWrite(STP, HIGH);
  delayMicroseconds (MeioPeriodo);
}

void FULL()
{
  digitalWrite(MS1, LOW);
  digitalWrite(MS2, LOW);
  digitalWrite(MS3, LOW);
}
void P1_8()
{
  digitalWrite(MS1, HIGH);
  digitalWrite(MS2, HIGH);
  digitalWrite(MS3, LOW);
}

void TesteMotor()
{
  ena_A4988();
  
  FULL(); 
  if(cont == true){
    HOR();delay(50);
    for (int i = 0; i <= 10; i++){PASSO();}
    AHR();delay(50);
    for (int i = 0; i <= 10; i++){PASSO();}
    HOR();delay(50);
    cont=false;
  }else{
    AHR();delay(50);
    for (int i = 0; i <= 10; i++){PASSO();}
    HOR();delay(50);
    for (int i = 0; i <= 10; i++){PASSO();}
    AHR();delay(50);
    cont=true;
  }

  delay(100);
  
  P1_8();
  for (int i = 0; i <= 230; i++){PASSO();}
  
  disa_A4988();
}

void loop()
{
  delay(1000);
  TesteMotor();      // Inicia teste do motor
}