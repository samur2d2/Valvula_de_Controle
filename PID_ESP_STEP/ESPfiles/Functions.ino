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

String concatWord(String horaCompletaToSend, String inputToSend){
  return (String(mqttClient) + "/" +dataSender+ "/" +horaCompletaToSend+ "/input/" +inputToSend);
}

void CalculaPID(){
  Input=Output;

  if((Setpoint != Input+1) || (Setpoint != Input-1)){
    erroAtual = Setpoint-Input;
    somatorioErro+=erroAtual;
    ganhoKp=erroAtual*Kp;
    ganhoKi=somatorioErro*Ki;
    
    Output=abs(ganhoKp+ganhoKi);
  }else{
    Output=Setpoint;
  }
}