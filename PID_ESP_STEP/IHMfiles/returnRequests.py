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