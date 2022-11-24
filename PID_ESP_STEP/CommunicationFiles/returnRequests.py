import socket
import os

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

def VerifyDir(IPSender):
    if (os.path.exists("../ArquivosHistorico/"+IPSender)) != True:
        os.makedirs("../ArquivosHistorico/"+IPSender)
    return "../ArquivosHistorico/"+IPSender