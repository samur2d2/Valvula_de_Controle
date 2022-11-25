import matplotlib.pyplot as plotter
from matplotlib.animation import FuncAnimation
import returnRequests as Request

with open("../IHMfiles/fileIP.txt", 'r') as fonte:
    IpOnFile = fonte.read()
    folder = Request.VerifyDir(IpOnFile)

day, hour = Request.getTime()
lerDadosPID = folder[0:]+ "/input_" +day+ ".txt"
lerDadosSET = folder[0:]+ "/setpoint_" +day+ ".txt"
dadosLast = folder[0:]+ "/LASTinput_" +day+ ".txt"


def Grafico():
    fig, ax = plotter.subplots()
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.25)
    fig.set_figheight(4)
    fig.set_figwidth(12)
    def animar(i):
        xPID, yPID = [], []
        xSET, ySET = [], []

        with open(lerDadosPID, 'r') as fonte:
            dadosPID = fonte.read()
        for linha in dadosPID.split('\n'):
            if len(linha) == 0:
                continue
            for dadosLinha in linha.split('; '):
                xi, yi = dadosLinha.split(',')
                xPID.append(xi)
                try:
                    yPID.append(float(yi))
                except:
                    yPID.append(0)

        with open(lerDadosSET, 'r') as fonte:
            dadosSET = fonte.read()
        for linha in dadosSET.split('\n'):
            if len(linha) == 0:
                continue
            for dadosLinha in linha.split('; '):
                xi, yi = dadosLinha.split(',')
                xSET.append(xi)
                try:
                    ySET.append(float(yi))
                except:
                    ySET.append(0)

        ax.clear()
        ax.plot(xSET,ySET)
        ax.plot(xPID,yPID) 

        for tick in ax.get_xticklabels(): 
            tick.set_rotation(90)

        last = open(dadosLast, 'r')
        lastWrite = last.read()
        last.close()

        limSupHora = lastWrite[0:2]
        limSupMin = lastWrite[3:5]
        limSupSec = lastWrite[6:8]
        limInfHora = ""
        limInfMin = ""
        limInfSec = ""

        if int(limSupSec) >= 30:
            limInfMin = limSupMin
            limInfHora = limSupHora
            if int(limSupSec) < 40:
                limInfSec = str("0"+str(int(limSupSec)-30))
            else:
                limInfSec = str(int(limSupSec)-30)
        else:
            if int(limSupMin) > 0:
                faltando = 30-int(limSupSec)
                limInfSec = str(60-faltando)
                limInfHora = limSupHora
                if int(limSupMin) >= 10:
                    limInfMin = str(int(limSupMin)-1)
                else:
                    limInfMin = str("0"+str(int(limSupMin)-1))
            else:
                limInfHora = "00"
                limInfMin = "00"
                limInfSec = "00"

        plotter.xlim(limInfHora+":"+limInfMin+":"+limInfSec, limSupHora+":"+limSupMin+":"+limSupSec)
    ani = FuncAnimation(fig, animar, interval = 1000)
    plotter.show()

#Grafico()