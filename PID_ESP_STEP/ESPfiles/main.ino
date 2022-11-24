//==================================================== BIBLIOTECAS ========================
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
//==================================================== TIMERS =============================
unsigned long previousMillis = 0;
const long interval = 1000;
#define timeBTWsend 1000
//==================================================== WIFI AND MQTT CONNECTIONS ==========
//#define ssid "CLARO_2G14C0A1" 
//#define password "Batatafrita16"
#define ssid "iniciacao" 
#define password "12345678"
#define mqttClient "192.168.0.10"
#define serverIP "192.168.1.100"
#define port 1883
//#define mqtt_user ""
//#define mqtt_password ""
//==================================================== MQTT DEFINES =======================
#define dataToRefPy "dataToRefPy"
#define personalTopic "192.168.0.10"
#define geralMessage "geral"
#define handShake "pyCommands"
//==================================================== MQTT CLIENT OBJECT =================
unsigned long current_time;
unsigned long last_send = 0;
WiFiClient espClient;
PubSubClient client(espClient);
//==================================================== MQTT MESSENGERS ====================
String IpSender="", dataSender="", horaSender="", typeSender ="", valueSender="";
String msgToSend = "";
String randomValue = "";
String mensagemRecebida = "";
//==================================================== PID VARIABLES ======================
double erroAtual, somatorioErro=0, ganhoKp, ganhoKi;
double Setpoint, Input, Output, oldContInterrupt;
double Kp=0.4, Ki=0.35;
volatile double contInterrupt = 0;
double vazaoMax=30, vazaoMin=0;
bool somaSubDaRef=false;
int referencia=0, limitePassos=5000, LiberarCalculoPID=0;
double intOut, oldOut, diferenca;
//==================================================== GLOBAL VARIABLES ===================
String refHoraSTR="", refMinSTR="", refSecSTR="";
int refHora=0, refMin=0, refSec=0;
bool sincronized = false;
//==================================================== PINOUT DEFINITIONS =================
int RST = D8, SLP = D1,  ENA = D7, MS1 = D4, MS2 = D5, MS3 = D6, DIR = D3, STP = D2;
const int sensor=10;
int MeioPeriodo = 3000;
//=========================================================================================
void setup()
{
  Serial.begin(115200);
  pinMode(SLP, OUTPUT);pinMode(ENA, OUTPUT);pinMode(MS1, OUTPUT);pinMode(MS2, OUTPUT);pinMode(MS3, OUTPUT);pinMode(DIR, OUTPUT);pinMode(STP, OUTPUT);pinMode(RST, OUTPUT);
  digitalWrite(SLP, HIGH);
  disa_A4988();
  rst_A4988();
  pinMode(sensor, INPUT);
  Setpoint=20;
  client.setServer(serverIP, port);
  client.setCallback(callback);
  setup_wifi();
  delay(500);
  //AHR();
  //TesteMotor(limitePassos);
}
//=========================================================================================
void loop()
{
  if(!client.connected()) {
    reconnect();   
  }
  client.loop();
  
  if(millis() - previousMillis >= 1000){
    previousMillis = millis();
    LiberarCalculoPID++;
    if(LiberarCalculoPID == 2){
      LiberarCalculoPID=0;
      oldContInterrupt = contInterrupt;   
       
      CalculaPID();

      Serial.print("Setpoint: ");
      Serial.println(Setpoint);
      Serial.print("Interrupcoes: ");
      Serial.println(contInterrupt);
      
      if((Setpoint == Input) || (Setpoint == Input+1) || (Setpoint == Input-1)){
      }else{
        if(Setpoint > Input){
          HOR(); //abre
          somaSubDaRef=false; //subtrai
          Serial.println("ABRE");
        }else if(Setpoint < Input){
          AHR(); //fecha
          somaSubDaRef=true; //soma
          Serial.println("FECHA");
        }
        int passos=map(Output,0,vazaoMax,0,500);
        Serial.print("Passos: ");
        Serial.println(passos);
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
      
      if(sincronized == true){
        msgToSend = concatWord(IncrementTime(), String(randomValue));
        client.publish("message", msgToSend.c_str());
      }
  
      oldOut=intOut;
    }
    contInterrupt=0;
  }
}