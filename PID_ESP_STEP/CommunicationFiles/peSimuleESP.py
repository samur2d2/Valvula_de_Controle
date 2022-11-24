import paho.mqtt.client as mqtt
import returnRequests as Functions
import time

broker = Functions.getIP()
port = 1883
handShake = "dataToRefPy"
personalTopic = "192.168.0.11"
message = "message"
client_id = "192.168.0.11"

timer=[0,0,0,"","","","",""] #[hhInt, mmInt, ssInt, hhStr, mmStr, ssStr, horaCompleta, dia]


def on_connect(client, userdata, flags, rc):
    print("[STATUS] Connected to Broker.")
    client.subscribe(personalTopic)
    mensagem=personalTopic+"/espSinc"
    publish(client, handShake, mensagem)

def on_message(client, userdata, msg):
    msgRecieved = str(msg.payload)[2:-1]
    IPSender, timer[7], hour, valor = msgRecieved.split("/")
    print("Message from " + IPSender + ": " + msgRecieved)
    timer[0],timer[1],timer[2] = hour.split(":")
    timer[0],timer[1],timer[2] = int(timer[0]), int(timer[1]), int(timer[2])

def publish(client, topicToSend, dataToSend):
    result = client.publish(topicToSend, dataToSend)
    status = result[0]
    if status == 0:
        print(f"Sent `{dataToSend}` to topic `{topicToSend}`")
    else:
        print(f"Failed to send message to topic {topicToSend}")

try:
    print("[STATUS] Starting MQTT...")
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    client.loop_start()
    while True:
        time.sleep(1)
        if timer[0]<10:
            timer[3]="0"+str(timer[0])
        else:
            timer[3]=str(timer[0])
        if timer[1]<10:
            timer[4]="0"+str(timer[1])
        else:
            timer[4]=str(timer[1])
        if timer[2]<10:
            timer[5]="0"+str(timer[2])
        else:
            timer[5]=str(timer[2])
            
        timer[6]=timer[3]+":"+timer[4]+":"+timer[5]
        publish(client, message, personalTopic+"/"+timer[7]+"/"+timer[6]+"/oi")
        if timer[2]==59:
            timer[2]=0
            timer[1]=timer[1]+1
            if timer[1]==59:
                timer[1]=0
                timer[0]=timer[0]+1
        else:
            timer[2]=timer[2]+1
        
    
except:
    print("Error")