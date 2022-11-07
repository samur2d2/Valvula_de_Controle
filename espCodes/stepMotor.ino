void rst_A4988(){
  digitalWrite(RST, LOW);
  digitalWrite(RST, HIGH);
}
//=========================================================================================
void disa_A4988(){digitalWrite(ENA, HIGH);}
void ena_A4988(){digitalWrite(ENA, LOW);}
void HOR(){digitalWrite(DIR, HIGH);}
void AHR(){digitalWrite(DIR, LOW);}
//=========================================================================================
void PASSO(){
  digitalWrite(STP, LOW);
  delayMicroseconds (MeioPeriodo);
  digitalWrite(STP, HIGH);
  delayMicroseconds (MeioPeriodo);
}
//=========================================================================================
void FULL(){
  digitalWrite(MS1, LOW);
  digitalWrite(MS2, LOW);
  digitalWrite(MS3, LOW);
}
//=========================================================================================
void P1_8(){
  digitalWrite(MS1, HIGH);
  digitalWrite(MS2, HIGH);
  digitalWrite(MS3, LOW);
}
//=========================================================================================
void TesteMotor(int nPassos){
  ena_A4988();
  FULL(); 
  if(cont == true){
    HOR();delay(50);
    for (int i=0; i<=10; i++){PASSO();}
    AHR();delay(50);
    for (int i=0; i<=10; i++){PASSO();}
    HOR();delay(50);
    cont=false;
  }else{
    AHR();delay(50);
    for (int i=0; i<=10; i++){PASSO();}
    HOR();delay(50);
    for (int i=0; i<=10; i++){PASSO();}
    AHR();delay(50);
    cont=true;
  }
  delay(100);
  P1_8();
  for (int i=0; i<=nPassos; i++){PASSO();}
  disa_A4988();
}