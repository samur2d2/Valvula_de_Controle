import paho.mqtt.client as mqtt
import returnRequests as Functions

broker = Functions.getIP()
port = 1883
client_id = "WatchAll"
KeepAliveBroker = 60

subs=["192.168.0.10", "192.168.0.11", "178.10.0.10", "message"]
excludes=["sinc"]

def on_connect(client, userdata, flags, rc):
    print("[STATUS] Connected to Broker.")
    for item in subs:
        client.subscribe(item)

def on_message(client, userdata, msg):
    msgRecieved = str(msg.payload)[2:-1]
    print("From topic '" +msg.topic+ "' - " + msgRecieved)
    ip, eventDay, eventHour, eventType, eventValue = msgRecieved.split("/")
    if ip!="sinc":
        folder = Functions.VerifyDir(ip)
        file = folder+"/"+eventType+"_"+eventDay+".txt"
        fileLast = folder+"/LAST"+eventType+"_"+eventDay+".txt"
        try:
            with open(fileLast, 'r+') as fonte:
                lastMinute = fonte.read()[3:5]
        except:
            open(fileLast, 'w')
        try:
            with open(file, 'r+') as fonte:
                data = fonte.read()
                if data == "":
                    fonte.write(eventHour+","+eventValue+";")
                elif eventHour[6:8] == "00" or lastMinute != eventHour[3:5]:
                    fonte.write("\n"+eventHour+","+eventValue+";")
                else:
                    fonte.write(" "+eventHour+","+eventValue+";")
        except:
            open(file, 'w')
        with open(fileLast, 'w') as fonte:
            fonte.write(eventHour)


try:
    print("[STATUS] Starting MQTT...")
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, KeepAliveBroker)
    client.loop_forever()
except:
    print("Error")