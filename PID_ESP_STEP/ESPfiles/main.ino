//==================================================== BIBLIOTECAS ========================
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
//==================================================== TIMERS =============================
unsigned long previousMillis = 0;
const long interval = 1000;
#define timeBTWsend 1000
//==================================================== WIFI AND MQTT CONNECTIONS ==========
#define ssid "CLARO_2G14C0A1" 
#define password "Batatafrita16"
#define mqttClient "0.0.0.1"
#define serverIP "192.168.0.249"
#define port 1883
//#define mqtt_user ""
//#define mqtt_password ""
//==================================================== MQTT DEFINES =======================
#define dataToRefPySUB "dataToRefPySUB"
#define personalTopic "0.0.0.1"
#define geralMessage "geral"
#define handShake "pyCommands"
//==================================================== MQTT CLIENT OBJECT =================
unsigned long current_time;
unsigned long last_send = 0;
WiFiClient espClient;
PubSubClient client(espClient);
//==================================================== MQTT MESSENGERS ====================
String IpSender="", dataSender="", horaSender="", valueSender="";
String msgToSend = "";
String randomValue = "";
String mensagemRecebida = "";
//==================================================== GLOBAL VARIABLES ===================
String refHoraSTR="", refMinSTR="", refSecSTR="";
int refHora=0, refMin=0, refSec=0;
bool sincronized = false;
//==================================================== PINOUT DEFINITIONS =================
int RST = D8, SLP = D1,  ENA = D7, MS1 = D4, MS2 = D5, MS3 = D6, DIR = D3, STP = D2;
int MeioPeriodo = 3000;
//=========================================================================================
void setup()
{
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
  Serial.begin(57600);
  client.setServer(serverIP, port);
  client.setCallback(callback);
  setup_wifi();
  delay(1500);
}
//=========================================================================================
void loop()
{
  if(!client.connected()) {
    reconnect();   
  }
  client.loop();
  
  if(sincronized == true){
    if(millis() - previousMillis >= 1000){
      previousMillis = millis();
      String horaCompletaToSend = IncrementTime();
      Serial.println(horaCompletaToSend);
      int randomValue = random(0, 20);
      msgToSend = "0.0.0.1/" + dataSender + "/" + horaCompletaToSend + "/" + String(randomValue);
      Serial.println(msgToSend);
      client.publish("message", msgToSend.c_str());
    }
  }
}