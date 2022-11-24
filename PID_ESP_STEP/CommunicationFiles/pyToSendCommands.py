import paho.mqtt.client as mqtt
from datetime import datetime
import returnRequests as Functions
import threading

broker = Functions.getIP()
port = 1883
commands = "pyCommands" 
client_id = "pyCommandsClient"
KeepAliveBroker = 60

respondeu = [False]

def on_connect(client, userdata, flags, rc):
    print("[STATUS] Connected to Broker.")
    client.subscribe(commands)

def on_message(client, userdata, msg):
    msgRecieved = str(msg.payload)[2:-1]
    IPSender, mensagem = msgRecieved.split("/")
    

def publish(client, ipToReply, dataToReply):
    client.publish(ipToReply, dataToReply)

def Ping():
    while True:
        text = input()
        
        now = str(datetime.now())
        day, hour = now.split(" ")
        hourSent=hour[0: 8]
        day=day.replace("-", "_")
        ip, command = text.split(" ")
        parameter, value = command.split("=")
        result = client.publish(ip, "terminalInput/"+day+"/"+hourSent+"/"+parameter+"/"+value)[0]
        if result == 0:
            print("Sent "+command+ "=" +command+ " to "+ip+".")
        else:
            print("Fail to communicate with the broker")
                

try:
    print("[STATUS] Starting MQTT...")
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, KeepAliveBroker)
    threading.Thread(target=Ping).start()
    client.loop_forever()
    
except:
    print("Error")