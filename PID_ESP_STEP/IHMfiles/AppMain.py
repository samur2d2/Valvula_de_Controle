from GraficoOline import Grafico
import returnRequests as Request
import paho.mqtt.client as mqtt
from tkinter import ttk
from tkinter import *
from MQTTPub import *
import threading
import sys


#===========================================MENU CONECTAR===========================================
def MQTTSub():
    Broker = "192.168.0.68"
    PortaBroker = 1883
    KeepAliveBroker = 60
    topic = "message" 
    def on_connect(client, userdata, flags, rc):
        print("[STATUS] Connected to Broker.")
        client.subscribe(topic)
    def on_message(client, userdata, msg):
        msgRecieved = str(msg.payload)[2:-1]
        print("Message from "+msg.topic+": "+msgRecieved)
        ip, eventDay, eventHour, eventType, eventValue = msgRecieved.split("/")
        if eventType == "input":
            presentValue.set(float(eventValue))
    try:
        print("[STATUS] Starting MQTT...")
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(Broker, PortaBroker, KeepAliveBroker)
        client.loop_forever()
    except KeyboardInterrupt:
        sys.exit(0)
#===========================================MENU CONECTAR===========================================

color1 = "#C6DEFF"
personalIP = "172.10.0.10"

app = Tk()
app.title("App")
app.geometry("360x480")

nb=ttk.Notebook(app)
nb.place(x=0, y=0, width=360, height=480)

abaConectar = Frame(nb, bg=color1)
abaDefinicoes = Frame(nb, bg=color1)
abaconfigurarMqtt = Frame(nb, bg=color1)

nb.add(abaConectar, text = "Conectar")
nb.add(abaDefinicoes, text = "Definicoes")
nb.add(abaconfigurarMqtt, text = "Configs")

#===========================================MENU CONECTAR===========================================
varAuxConnected = StringVar()
varAuxConnected.set("Disconnected")

def Send():
    day, hourSent = Request.getTime()
    stringToSend = str("ihm/" + day + "/" + hourSent + "/setpoint/" + str(setPoint.get()))
    Sent(stringToSend, str(ipNum.get()), int(portNum.get()), str(espIP.get()), str(clientPubName.get()))
    setPoint.set(setPoint.get())


def TurnOn():
    day, hourSent = Request.getTime()
    stringToSend = str("ihm/" + day + "/" + hourSent + "/pid/1")
    Sent(stringToSend, str(ipNum.get()), int(portNum.get()), str(espIP.get()), str(clientPubName.get()))

def TurnOff():
    day, hourSent = Request.getTime()
    stringToSend = str("ihm/" + day + "/" + hourSent + "/pid/0")
    Sent(stringToSend, str(ipNum.get()), int(portNum.get()), str(espIP.get()), str(clientPubName.get()))


def SoftStart():
    day, hourSent = Request.getTime()
    stringToSend = str("ihm/" + day + "/" + hourSent + "/motor/soft")
    Sent(stringToSend, str(ipNum.get()), int(portNum.get()), str(espIP.get()), str(clientPubName.get()))

def ChamaGrafico():
    with open("./IHMfiles/fileIP.txt", 'w') as fonte:
        fonte.write(espIP.get())
    Grafico()


presentValue=DoubleVar()
presentValue.set(0.0)
objIpPosX, objIpPosY = 170, 50
labelSetpoint = Label(abaConectar, text="PV:", font=("Calibri", 16), bg=color1).place(x=objIpPosX, y=objIpPosY)
entrySetpoint = Entry(abaConectar, width=6, textvariable=presentValue, font=("Calibri", 16), justify=RIGHT).place(x=objIpPosX+35, y=objIpPosY+3)

setPoint=DoubleVar()
setPoint.set(0.0)
objIpPosX, objIpPosY = objIpPosX+2, objIpPosY+35
labelSetPoint = Label(abaConectar, text="ST:", font=("Calibri", 16), bg=color1).place(x=objIpPosX, y=objIpPosY)
entrySetPoint = Entry(abaConectar, width=6, textvariable=setPoint, font=("Calibri", 16), justify=RIGHT).place(x=objIpPosX+33, y=objIpPosY+3)

botaoSend = Button(abaConectar, text="✓", command=Send, font=("Calibri", 10)).place(x=objIpPosX+115, y=objIpPosY+7)


objIpPosX, objIpPosY = 140, 200
botaoTurnOn = Button(abaConectar, text="Turn On", command=TurnOn, font=("Calibri", 12)).place(x=objIpPosX, y=objIpPosY)
botaoTurnOff = Button(abaConectar, text="Turn Off", command=TurnOff, font=("Calibri", 12)).place(x=objIpPosX+70, y=objIpPosY)
#botaoSoftStart = Button(abaConectar, text="Soft Start", command=SoftStart, font=("Calibri", 12)).place(x=objIpPosX+142, y=objIpPosY)


botaoGrafico = Button(abaConectar, text="Grafico", command=ChamaGrafico, font=("Calibri", 16)).place(x=250, y=350)


objIpPosX, objIpPosY = 10, 430
labelLegenda = Label(abaConectar, text="status: ", font=("Calibri", 10), bg=color1).place(x=objIpPosX, y=objIpPosY)
labelLegenda = Label(abaConectar, text=varAuxConnected.get(), font=("Calibri", 10), bg=color1).place(x=objIpPosX+40, y=objIpPosY)

#===========================================MENU DEFINICOES===========================================

def AttKp():
    day, hourSent = Request.getTime()
    stringToSend = str("ihm/" + day + "/" + hourSent + "/kp/" + str(KpValue.get()))
    Sent(stringToSend, str(ipNum.get()), int(portNum.get()), str(espIP.get()), str(clientPubName.get()))
    KpValue.set(KpValue.get())

def AttKi():
    day, hourSent = Request.getTime()
    stringToSend = str("ihm/" + day + "/" + hourSent + "/ki/" + str(KiValue.get()))
    Sent(stringToSend, str(ipNum.get()), int(portNum.get()), str(espIP.get()), str(clientPubName.get()))
    KiValue.set(KiValue.get())

def AttKd():
    day, hourSent = Request.getTime()
    stringToSend = str("ihm/" + day + "/" + hourSent + "/kd/" + str(KdValue.get()))
    Sent(stringToSend, str(ipNum.get()), int(portNum.get()), str(espIP.get()), str(clientPubName.get()))
    KdValue.set(KdValue.get())


KpValue=DoubleVar()
KpValue.set(0.4)
objIpPosX, objIpPosY = 20, 10
labelKpValue = Label(abaDefinicoes, text="Kp:", font=("Calibri", 14), bg=color1).place(x=objIpPosX, y=objIpPosY)
entryKpValue = Entry(abaDefinicoes, width=5, textvariable=KpValue, font=("Calibri", 14), justify=RIGHT, state=DISABLED).place(x=objIpPosX, y=objIpPosY+25)

botaoAtualizar = Button(abaDefinicoes, text="Atualizar", command=AttKp, state=DISABLED).place(x=objIpPosX+65, y=objIpPosY+27)

KiValue=DoubleVar()
KiValue.set(0.5)
objIpPosX, objIpPosY = 20, objIpPosY+55
labelKiValue = Label(abaDefinicoes, text="Ki:", font=("Calibri", 14), bg=color1).place(x=objIpPosX, y=objIpPosY)
entryKiValue = Entry(abaDefinicoes, width=5, textvariable=KiValue, font=("Calibri", 14), justify=RIGHT, state=DISABLED).place(x=objIpPosX, y=objIpPosY+25)

botaoAtualizar = Button(abaDefinicoes, text="Atualizar", command=AttKi, state=DISABLED).place(x=objIpPosX+65, y=objIpPosY+27)

KdValue=DoubleVar()
KdValue.set(0.0)
objIpPosX, objIpPosY = 20, objIpPosY+55
labelKdValue = Label(abaDefinicoes, text="Kd:", font=("Calibri", 14), bg=color1).place(x=objIpPosX, y=objIpPosY)
entryKdValue = Entry(abaDefinicoes, width=5, textvariable=KdValue, font=("Calibri", 14), justify=RIGHT, state=DISABLED).place(x=objIpPosX, y=objIpPosY+25)

botaoAtualizar = Button(abaDefinicoes, text="Atualizar", command=AttKd, state=DISABLED).place(x=objIpPosX+65, y=objIpPosY+27)


objIpPosX, objIpPosY = 20, 330
labelLegenda = Label(abaDefinicoes, text="Kp - Ganho proporcional", font=("Calibri", 10), bg=color1).place(x=objIpPosX, y=objIpPosY)
labelLegenda = Label(abaDefinicoes, text="Ki - Ganho integrativo", font=("Calibri", 10), bg=color1).place(x=objIpPosX, y=objIpPosY+20)
labelLegenda = Label(abaDefinicoes, text="Kd - Ganho derivativo", font=("Calibri", 10), bg=color1).place(x=objIpPosX, y=objIpPosY+40)

objIpPosX, objIpPosY = 10, 430
labelLegenda = Label(abaDefinicoes, text="status: ", font=("Calibri", 10), bg=color1).place(x=objIpPosX, y=objIpPosY)
labelLegenda = Label(abaDefinicoes, text=varAuxConnected.get(), font=("Calibri", 10), bg=color1).place(x=objIpPosX+40, y=objIpPosY)

#===========================================MENU CONFIGS===========================================

ipNum=StringVar()
ipNum.set(str(Request.getIP()))
objIpPosX, objIpPosY = 20, 10
labelIP = Label(abaconfigurarMqtt, text="Broker IP:", font=("Calibri", 14), bg=color1).place(x=objIpPosX, y=objIpPosY)
entryIP = Entry(abaconfigurarMqtt, width=12, textvariable=ipNum, font=("Calibri", 14), state=DISABLED).place(x=objIpPosX, y=objIpPosY+25)

portNum=StringVar()
portNum.set(1883)
objPortPosX, objPortPosY = 170, 10
labelPorta = Label(abaconfigurarMqtt, text="Porta:", font=("Calibri", 14), bg=color1).place(x=objPortPosX, y=objPortPosY)
entryPorta = Entry(abaconfigurarMqtt, textvariable=portNum, width=10, font=("Calibri", 14), state=DISABLED).place(x=objPortPosX, y=objPortPosY+25)

clientSubName=StringVar()
clientSubName.set("sampepePub")
objPubPosX, objPubPosY = 20, 80
labelClientPub = Label(abaconfigurarMqtt, text="Client Publisher:", font=("Calibri", 14), bg=color1).place(x=objPubPosX, y=objPubPosY)
entryClientPub = Entry(abaconfigurarMqtt, width=20, textvariable=clientSubName, font=("Calibri", 14), state=DISABLED).place(x=objPubPosX, y=objPubPosY+25)

clientPubName=StringVar()
clientPubName.set("sampepeSub")
objSubPosX, objSubPosY = 20, 135
labelClientSub = Label(abaconfigurarMqtt, text="Client Subscriber:", font=("Calibri", 14), bg=color1).place(x=objSubPosX, y=objSubPosY)
entryClientSub = Entry(abaconfigurarMqtt, width=20, textvariable=clientPubName, font=("Calibri", 14), state=DISABLED).place(x=objSubPosX, y=objSubPosY+25)

topicName=StringVar()
topicName.set("message")
objTopicPosX, objTopicPosY = 20, 220
labelTopic = Label(abaconfigurarMqtt, text="Tópico:", font=("Calibri", 14), bg=color1).place(x=objTopicPosX, y=objTopicPosY)
entryTopic = Entry(abaconfigurarMqtt, width=13, textvariable=topicName, font=("Calibri", 14), state=DISABLED).place(x=objTopicPosX, y=objTopicPosY+25)

espIP=StringVar()
espIP.set("192.168.0.10")
objTopicPosX, objTopicPosY = 170, 220
labelTopic = Label(abaconfigurarMqtt, text="Actuator IP:", font=("Calibri", 14), bg=color1).place(x=objTopicPosX, y=objTopicPosY)
entryTopic = Entry(abaconfigurarMqtt, width=15, textvariable=espIP, font=("Calibri", 14), state=DISABLED).place(x=objTopicPosX, y=objTopicPosY+25)

objIpPosX, objIpPosY = 10, 430
labelLegenda = Label(abaconfigurarMqtt, text="status: ", font=("Calibri", 10), bg=color1).place(x=objIpPosX, y=objIpPosY)
labelLegenda = Label(abaconfigurarMqtt, text=varAuxConnected.get(), font=("Calibri", 10), bg=color1).place(x=objIpPosX+40, y=objIpPosY)



threading.Thread(target=MQTTSub).start()
app.mainloop()