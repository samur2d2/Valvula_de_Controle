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
  Serial.println(nPassos);
  ena_A4988();
  
  P1_8();
  
  delay(10);
  P1_8();
  for (int i=0; i<=nPassos; i++){PASSO();delay(1);}
  delay(10);
  disa_A4988();
}