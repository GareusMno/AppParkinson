import time
import hashlib
import sys 

from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication,QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from pathlib import Path

from main import BD
sys.path.append( '.' )

class MainWindow(QMainWindow):
    paciente=""
    laps={0:'null',
             1:'null',
             2:'null',
    }
    def __init__(self, *args, **kwargs):
        self.BDatos = BD.Base()
        self.lap=1
        self.comienzo = 0
        self.tiempo = 0
        self.count = 0
        self.flag = False
        super().__init__(*args, **kwargs)
        self.interfaz = uic.loadUi("ui/Cronometro.ui", self)
        self.interfaz.Start.pressed.connect(self.estadoBotonCronometro)
        self.interfaz.Reset.pressed.connect(self.Re_set)
        self.interfaz.Guardar.pressed.connect(self.guardarTiempo)
        self.interfaz.nombre_paciente.setText(self.paciente)
        self.Cronometro.setFont(QFont('Arial', 25))
        # creating a timer object 
        timer = QTimer(self.interfaz.VentanaCrono) 
        # adding action to timer 
        timer.timeout.connect(self.showTime) 
        # update the timer every tenth second 
        timer.start(50) 
        self.vez=0
        self.continuar=0
        self.interfaz.show()

    def estadoBotonCronometro(self):
        if (self.Start.text()=="Start"):
            self.Re_set()
            self.Start.setText("Lap %d" % self.lap)
            self.start()
        elif(self.Start.text()=="Lap 3"):
            self.CalcularLap
            self.Start.setText("Start")
            self.Tiempo_v_3.setText(self.Cronometro.text())
            self.pause()
        else:
            self.CalcularLap()
            self.Start.setText("Lap %d" % self.lap)

    def start(self):
        # making flag to true
            if (self.vez==0):
                self.vez=1
                self.comienzo = time.perf_counter()
                self.flag = True
            elif(self.vez==2):
                self.vez=1
                self.continuar = time.perf_counter()-self.pausado+self.continuar
                self.flag = True
                
    def pause(self): 
        self.flag = False
        self.pausado = time.perf_counter()
        self.vez=2
        
    def CalcularLap(self):
        self.laps[self.lap]=self.Cronometro.text()
        if (self.Tiempo_v_1.text()==""):
            self.Tiempo_v_1.setText(self.Cronometro.text())
        elif (self.Tiempo_v_2.text()==""):
            self.Tiempo_v_2.setText(self.Cronometro.text())
            
        self.lap=self.lap+1
    def Re_set(self): 
        # making flag to false 
        self.flag = False
        self.vez=0
        self.continuar=0
        # reseeting the count 
        self.count = 0
        self.lap=1
        self.interfaz.Start.setText("Start")
        self.Tiempo_v_1.setText("")
        self.Tiempo_v_2.setText("")
        self.Tiempo_v_3.setText("")
        # setting text to label 
        self.Cronometro.setText(str(self.count)) 
    def guardarTiempo(self):
        self.BDatos.sql_GuardarPrueba(self.paciente,self.Cronometro.text())
    def showTime(self): 
        # checking if flag is true 
        if self.flag: 
            # incrementing the counter 
            self.count=round(time.perf_counter()-(self.comienzo+self.continuar),2)
            
        # getting text from count 
        text = str(self.count) 
        # showing text 
        self.Cronometro.setText(text) 