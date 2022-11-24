//=========================================================================================
void reconnect() {
  while (!client.connected()) {
    Serial.print("Trying to connect to MQTT Broker... ");
    if (client.connect(mqttClient)) {
      Serial.println("connected");
      client.subscribe(personalTopic);
      client.subscribe(geralMessage);
      
      String msgToSend = String(mqttClient)+"/espSinc";
      client.publish(dataToRefPySUB, msgToSend.c_str());
      Serial.println("Published " + msgToSend + " to topic " + dataToRefPySUB);
    }else{
      Serial.print("connection failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 3 seconds");
      delay(3000);
    }
  }
}
//=========================================================================================
void callback(char* topic, byte* payload, unsigned int length){
  mensagemRecebida = "";
  Serial.print("Message arrived: ");
  for (int i=0;i<length;i++) {
    mensagemRecebida += (char)payload[i];
  }
  Serial.println(mensagemRecebida);

  int firstParameter=0;
  String parameter="", value="";
  IpSender=""; dataSender=""; horaSender=""; valueSender="";
   
  for(int i=0; i<mensagemRecebida.length(); i++){
    if(mensagemRecebida[i]=='/'){firstParameter++;i++;}
    if(firstParameter == 0){IpSender += mensagemRecebida[i];}
    else if(firstParameter == 1){dataSender += mensagemRecebida[i];}
    else if(firstParameter == 2){horaSender += mensagemRecebida[i];}
    else if(firstParameter == 3){valueSender += mensagemRecebida[i];}
  }

  Serial.print("IP: ");
  Serial.println(IpSender);
  Serial.print("Data: ");
  Serial.println(dataSender);
  Serial.print("Hora: ");
  Serial.println(horaSender);
  Serial.print("Valor: ");
  Serial.println(valueSender);
  if(IpSender=="step"){
    if(valueSender[0] == '+'){
      Serial.print("Sentido horario: ");
      HOR();
    }else if(valueSender[0] == '-'){
      AHR();
      Serial.print("Sentido anti-Horario: ");
    }
    valueSender.remove(0,1);
    TesteMotor(valueSender.toInt());
  }else if(IpSender=="sinc"){
    refHoraSTR = horaSender[0]; refHoraSTR += horaSender[1];
    refMinSTR = horaSender[3]; refMinSTR += horaSender[4];
    refSecSTR = horaSender[6]; refSecSTR += horaSender[7];
    refHora = refHoraSTR.toInt();
    refMin = refMinSTR.toInt();
    refSec = refSecSTR.toInt();
    sincronized=true;
  }
  
}
//=========================================================================================