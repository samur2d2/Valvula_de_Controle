from paho.mqtt import client as mqtt_client
import time

brokerIp = "192.168.0.68"
portNum = 1883
KeepAliveBroker = 60
topicName = "mensagem" 
clientName = "sub"


client = mqtt_client.Client(clientName)  

def connect_mqtt(brokerIp, clientName, portNum):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client.on_connect = on_connect
    client.connect(brokerIp, portNum)
    return client

def on_message(client, userdata, msg):
    mensagem = msg.payload.decode()
    print(f"Received `{mensagem}` from `{topicName}`")
    

def conectar(brokerIp, clientName, portNum): 
    client = connect_mqtt(brokerIp, clientName, portNum)
    client.loop_start()
    client.loop_stop()
    varAuxConnected = "tt"
    return varAuxConnected


def run():
    client.loop_start()
    if client.subscribe("mensagem") == 'None':
        pass
    else:
        client.on_message = on_message
    client.loop_stop()


