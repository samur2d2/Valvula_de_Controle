#include <ESP8266WiFi.h>
#include <PubSubClient.h>
//=========================================================================================
unsigned long previousMillis = 0;
const long interval = 1000;
#define timeBTWsend 1000
//=========================================================================================
#define ssid "CLARO_2G14C0A1" 
#define password "Batatafrita16"
#define mqttClient "0.0.0.1"
#define serverIP "192.168.0.68"
#define port 1883
//#define mqtt_user ""
//#define mqtt_password ""
//=========================================================================================
#define dataToRefPySUB "dataToRefPySUB"
#define personalTopic "0.0.0.1"
#define geralMessage "geral"
#define handShake "pyCommands"
//=========================================================================================
unsigned long current_time;
unsigned long last_send = 0;
WiFiClient espClient;
PubSubClient client(espClient);
//=========================================================================================
unsigned long startPingTimer = 0;
String msgToSinc = "";
String randomValue = "";
String mensagemRecebida = "";
//=========================================================================================
int RST = D8, SLP = D1,  ENA = D7, MS1 = D4, MS2 = D5, MS3 = D6, DIR = D3, STP = D2;
int MeioPeriodo = 3000;
bool cont = true;
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
  if (!client.connected()) {
    reconnect();   
  }
  client.loop();
}
