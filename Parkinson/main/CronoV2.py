import os
import sys 
import time
import hashlib


from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication,QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from pathlib import Path
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from main import BD,addUser,PacientesPruebaGrafica2

class MainWindow(QMainWindow):
    paciente=""
    laps={0:'null',
             1:'null',
             2:'null',
    }
    def __init__(self,bd):
        self.BDatos = BD.Base(bd)
        print(bd)
        self.lap=1
        self.comienzo = 0
        self.tiempo = 0
        self.count = 0
        self.flag = False
        super().__init__()
        self.interfaz = uic.loadUi(".."+os.path.sep+"ui"+os.path.sep+"CronometroReal.ui", self)
        self.interfaz.Start.pressed.connect(self.estadoBotonCronometro)
        self.interfaz.Reset.pressed.connect(self.Re_set)
        self.interfaz.Guardar.pressed.connect(self.guardarTiempo)
        self.interfaz.nombre_paciente.setText(self.paciente)
        self.Cronometro.setFont(QFont('Arial', 25))
        # Creamos el qtimer y lo conectamos a la función en la que se irá actualizando con el tiempo indicando
        timer = QTimer(self.interfaz.VentanaCrono) 
        timer.timeout.connect(self.showTime) 
        timer.start(50) 
        self.vez=0
        self.continuar=0
        self.interfaz.show()
    # Función que nos permitirá según el texto del boton (estado)
    # guardár el tiempo de cada segmento
    def estadoBotonCronometro(self):
        if (self.Start.text()=="Start"):
            self.Re_set()
            self.Start.setText("Lap %d" % self.lap)
            self.start()
        elif(self.Start.text()=="Lap 3"):
            self.CalcularLap
            self.Start.setText("Start")
            tiempo3 = float(self.Cronometro.text()) - float(self.Tiempo_v_2.text()) - float(self.Tiempo_v_1.text())
            self.Tiempo_v_3.setText(str(tiempo3))
            self.pause()
        else:
            self.CalcularLap()
            self.Start.setText("Lap %d" % self.lap)
    # Función que inicia el cronómetro y donde calculamos los tiempos 
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
    # Función que pausará el cronómetro cuando se acaben las vueltas
    def pause(self): 
        self.flag = False
        self.pausado = time.perf_counter()
        self.vez=2
    # Función que nos añadirá los tiempos según vamos cambiando de segmento
    # Para poder ver los tiempos guardados según está funcionando
    def CalcularLap(self):
        self.laps[self.lap]=self.Cronometro.text()
        if (self.Tiempo_v_1.text()==""):
            self.Tiempo_v_1.setText(self.Cronometro.text())
        elif (self.Tiempo_v_2.text()==""):
            tiempo2 = float(self.Cronometro.text()) - float(self.Tiempo_v_1.text())
            self.Tiempo_v_2.setText(str(tiempo2))
        self.lap=self.lap+1
    # Función que volverá todos los valores a su estado inicial
    # Para poder repetir la prueba
    def Re_set(self): 
        # making flag to false 
        self.flag = False
        self.vez=0
        self.continuar=0
        self.count = 0
        self.lap=1
        self.interfaz.Start.setText("Start")
        self.Tiempo_v_1.setText("")
        self.Tiempo_v_2.setText("")
        self.Tiempo_v_3.setText("")
        self.Cronometro.setText(str(self.count)) 
    # Función que nos permitirá enviar los datos de la vuelta
    # A nuestra base de datos y que además
    # Nos actualizará el paciente y cuando volvamos al paciente
    # Nos indicará que grado de enfermedad tiene actualmente
    # Según el tiempo total
    def guardarTiempo(self):
        total = float(self.Cronometro.text())
        self.BDatos.sql_GuardarPrueba(self.paciente,self.Tiempo_v_1.text(),self.Tiempo_v_2.text(),self.Tiempo_v_3.text(),self.Cronometro.text())
        clasi = self.BDatos.sql_getClasificacion()
        t1 = float(clasi[0][3])
        t2 = float(clasi[1][3])
        resultado=""
        if (total < t1):
            resultado="Leve"
            self.BDatos.sql_ActualizarGravedad(self.paciente,"Leve")
        if (total >=t1 and total <t2):
            resultado="Moderado"
            self.BDatos.sql_ActualizarGravedad(self.paciente,"Moderada")
        if (total >= t2):
            resultado="Grave"
            self.BDatos.sql_ActualizarGravedad(self.paciente,"Grave")
        self.addUserDialog = addUser.GuardarPrueba(resultado)
        self.addUserDialog.show()
        self.addUserDialog.exec_()
    # Función que nos enseña el tiempo total de la prueba según va avanzando
    def showTime(self): 
        if self.flag: 
            self.count=round(time.perf_counter()-(self.comienzo+self.continuar),2)
        text = str(self.count) 
        self.Cronometro.setText(text) 