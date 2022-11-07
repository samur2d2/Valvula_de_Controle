import time
import paho.mqtt.client as mqtt

broker = "192.168.0.68"
port = 1883
recievedTopic = "dataToRefPySUB" 
client_id = "PythonPubSub"
KeepAliveBroker = 60

lerDataLastData = "lastDataSaved.txt"

def on_connect(client, userdata, flags, rc):
    print("[STATUS] Connected to Broker.")
    client.subscribe(recievedTopic)

def on_message(client, userdata, msg):
    msgRecieved = str(msg.payload)[2:-1]
    IPSender, mesnsagem = msgRecieved.split("/")
    print("Message from " + IPSender + ": " + mesnsagem)
    if mesnsagem == "espSinc":
        time.sleep(0.5)
        publish(client, IPSender)

def publish(client, topicToRefPyPUB):
    with open(lerDataLastData, 'r') as fonte:
        lastDataSaved = fonte.read()
    msg = str("sinc="+lastDataSaved)
    result = client.publish(topicToRefPyPUB, msg)
    status = result[0]
    if status == 0:
        print(f"Sent `{msg}` to topic `{topicToRefPyPUB}`")
    else:
        print(f"Failed to send message to topic {topicToRefPyPUB}")

try:
    print("[STATUS] Starting MQTT...")
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, KeepAliveBroker)
    client.loop_forever()
    
except:
    print("Error")