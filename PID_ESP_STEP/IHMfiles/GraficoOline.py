import matplotlib.pyplot as plotter
from matplotlib.animation import FuncAnimation
import returnRequests as Request

with open("./IHMfiles/fileIP.txt", 'r') as fonte:
    IpOnFile = fonte.read()
    folder = Request.VerifyDir(IpOnFile)

day, hour = Request.getTime()
lerDadosPID = folder[1:]+ "/random_" +day+ ".txt"
lerDadosSET = folder[1:]+ "/setpoint_" +day+ ".txt"
dadosLast = folder[1:]+ "/LASTrandom_" +day+ ".txt"


def Grafico():
    fig, ax = plotter.subplots()

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
        for linha in dadosSET.split('; '):
            if len(linha) == 0:
                continue
            xi, yi = linha.split(',')
            xSET.append(xi)
            try:
                ySET.append(float(yi))
            except:
                ySET.append(0)

        ax.clear()
        ax.plot(xSET,ySET)
        ax.plot(xPID,yPID) 

        for tick in ax.get_xticklabels(): 
            tick.set_rotation(60)

        # last = open(dadosLast, 'r')
        # lastWrite = last.read()
        # last.close()

        # limSupHora = lastWrite[0:2]
        # limSupMin = lastWrite[3:5]
        # limSupSec = lastWrite[6:8]
        # limInfHora = ""
        # limInfMin = ""
        # limInfSec = ""

        # if int(limSupSec) >= 30:
        #     limInfMin = limSupMin
        #     limInfHora = limSupHora
        #     if int(limSupSec) < 40:
        #         limInfSec = str("0"+str(int(limSupSec)-30))
        #     else:
        #         limInfSec = str(int(limSupSec)-30)
        # else:
        #     if int(limSupMin) > 0:
        #         limInfMin = str("0"+str(int(limSupMin)-1))
        #         faltando = 30-int(limSupSec)
        #         limInfSec = str(60-faltando)
        #     else:
        #         limInfMin = "00"
        #         limInfSec = "00"
        #         if int(limSupHora) > 0:
        #             limInfHora = str(int(limInfHora)-1)
        #         else:
        #             limInfHora = "00"

        # plotter.xlim(limInfHora+":"+limInfMin+":"+limInfSec, limSupHora+":"+limSupMin+":"+limSupSec)
    ani = FuncAnimation(fig, animar, interval = 500)
    plotter.show()
