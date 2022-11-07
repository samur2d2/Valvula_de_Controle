//=========================================================================================
void reconnect() {
  while (!client.connected()) {
    Serial.print("Trying to connect to MQTT Broker... ");
    if (client.connect(mqttClient)) {
      Serial.println("connected");
      client.subscribe(personalTopic);
      client.subscribe(geralMessage);
      
      String msgToSinc = String(mqttClient)+"/espSinc";
      client.publish(dataToRefPySUB, msgToSinc.c_str());
      Serial.println("Published " + msgToSinc + " to topic " + dataToRefPySUB);
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

  bool firstParameter=false;
  String parameter="", value="";
  
  if(mensagemRecebida == "ping"){
    Ping();
  }
  else if(mensagemRecebida == "reping"){
    rePing();
  }
  else{
    for(int i=0; i<mensagemRecebida.length(); i++){
      if(mensagemRecebida[i]=='='){firstParameter=true;i++;}
      if(firstParameter == false){parameter += mensagemRecebida[i];}
      else{value += mensagemRecebida[i];}
    }
    if(parameter=="step"){
      if(value[0] == '+'){
        Serial.print("Horario: ");
        cont=true;
      }else if(value[0] == '-'){
        cont=false;
        Serial.print("Anti-Horario: ");
      }
      value.remove(0,1);
      TesteMotor(value.toInt());
    }
  }
}
//=========================================================================================
void Ping(){
  msgToSinc = String(mqttClient)+"/ping";
  client.publish(handShake, msgToSinc.c_str());
  Serial.println("Published " + msgToSinc + " to topic " + handShake);
  startPingTimer = millis();
}
//=========================================================================================
void rePing(){
  String pingTime = String((millis() - startPingTimer)/2);
  msgToSinc = String(mqttClient)+"/"+pingTime+" ms";
  client.publish(handShake, msgToSinc.c_str());
  Serial.println("Published " + msgToSinc + " to topic " + handShake);
}
