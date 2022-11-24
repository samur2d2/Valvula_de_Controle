import paho.mqtt.client as mqtt
from datetime import datetime
import returnRequests as Functions
import time

broker = Functions.getIP()
port = 1883
recievedTopic = "dataToRefPy" 
client_id = "PythonPubSub"
KeepAliveBroker = 60

def on_connect(client, userdata, flags, rc):
    print("[STATUS] Connected to Broker.")
    client.subscribe(recievedTopic)

def on_message(client, userdata, msg):
    msgRecieved = str(msg.payload)[2:-1]
    IPSender, mensagem = msgRecieved.split("/")
    print("Message from " + IPSender + ": " + mensagem)
    if mensagem == "espSinc":
        for i in range(10):
            now = str(datetime.now())
            day, hour = now.split(" ")
            hourSent=hour[0: 8]
            day=day.replace("-", "_")
            if(hour[9:10]=="0"):
                break
            time.sleep(0.1)
        publish(client, IPSender, day+"/"+hourSent+"/sinc/0")

def publish(client, topicToRefPy, msg):
    msg = str("sinc/"+msg)
    result = client.publish(topicToRefPy, msg)
    status = result[0]
    if status == 0:
        print(f"Sent `{msg}` to topic `{topicToRefPy}`")
    else:
        print(f"Failed to send message to topic {topicToRefPy}")


try:
    print("[STATUS] Starting MQTT...")
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, KeepAliveBroker)
    client.loop_forever()
    
except:
    print("Error")