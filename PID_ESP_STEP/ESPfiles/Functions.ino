IRAM_ATTR void SensorCctivated(){
  contInterrupt++;
}

String IncrementTime(){
  refSec++;
  if(refSec==60){
    refSec=0;
    refMin++;
  }
  if(refMin==60){
    refMin=0;
    refHora++;
  }
  if(refHora==24){
    refHora=0;
  }
  if(refSec<10){refSecSTR="0"; refSecSTR+=String(refSec);}
  else{refSecSTR = String(refSec);}
  if(refMin<10){refMinSTR="0"; refMinSTR+=String(refMin);}
  else{refMinSTR = String(refMin);}
  if(refHora<10){refHoraSTR="0"; refHoraSTR+=String(refHora);}
  else{refHoraSTR = String(refHora);}
  
  return(refHoraSTR+ ":" +refMinSTR+ ":" +refSecSTR);
}

String concatWord(String horaCompletaToSend, String randomValue){
  return (String(mqttClient) + "/" +dataSender+ "/" +horaCompletaToSend+ "/random/" +randomValue);
}

void CalculaPID(){
  Input=contInterrupt;

  if((Setpoint <= Input+1) && (Setpoint >= Input-1)){
    return;
  }

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