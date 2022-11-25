import socket
import os
from datetime import datetime

def getIP():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

def getTime():
    now = str(datetime.now())
    day, hour = now.split(" ")
    hourSent=hour[0: 8]
    day=day.replace("-", "_")
    return day, hourSent

def VerifyDir(IPSender):
    if (os.path.exists("../ArquivosHistorico/"+IPSender)) != True:
        os.makedirs("../ArquivosHistorico/"+IPSender)
    return "../ArquivosHistorico/"+IPSender

def SaveSetpoint(ip, eventDay, eventHour, eventType, eventValue):
    folder = VerifyDir(ip)
    file = folder+"/setpoint_" +eventDay+ ".txt"
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