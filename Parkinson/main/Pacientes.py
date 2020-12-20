import sys
import sqlite3
import hashlib
import os

from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication,QListWidgetItem,QFrame,QListWidget,QDialog,QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from pathlib import Path

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
sys.path.append( '.' )
from main import BD
from main import CronoV2

# Clase que utilizaremos para crear el lienzo
# Donde mostraremos los tiempos de los pacientes
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_color('black')
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
# Clase principal de la ventana de los pacientes
# Que nos mostrara una lista de cada paciente y segun el paciente
# Seleccionado nos mostrará sus datos y una gráfica con sus tiempos
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargamos la interfaz creada con QTDesigner 
        self.interfaz = uic.loadUi("ui/Pacientes.ui", self)
        #Creamos el objeto para trabar con la base de datos
        self.BDatos = BD.Base()
        #Conseguimos la lista de pacientes y la añadimos al combo box que cuando cambie de valor
        #Inciará la funcion que mostrara los datos del paciente y habilitará los botones
        self.lista_pacientes=self.BDatos.sql_getPacientes()
        self.interfaz.combo_pacientes.addItems(self.lista_pacientes)
        self.interfaz.combo_pacientes.currentTextChanged.connect(self.enableButtons)
        #Conectamos los botones con su respectiva funcion
        self.interfaz.prueba_crono.pressed.connect(self.RealizarPrueba)
        self.interfaz.AddPaciente.pressed.connect(self.BotonAddPaciente)
        self.interfaz.modificar_paciente.pressed.connect(self.Modificar)
        #Creamos la capa de la grafica y activamos la opción de actualizar para que cuando
        #Cambiemos entre pacientes podamos actualizar sus datos
        self.sc= MplCanvas(self, width=10, height=4, dpi=100)
        self.sc.setUpdatesEnabled(True)
        #Se ha implementado de forma manual, así que la añadimos al layout y mostramos la interfaz
        self.interfaz.verticalLayout.addWidget(self.sc)
        self.interfaz.show()
    # Función conectada la botón de modificar
    # Nos habilitará los campos del paciente para que podamos modificarlo
    # Además el mismo botón cambiará de nombre y nos servira para que una vez tengamos los campos
    # Como queremos los guardemos y actualizará la base de datos
    def Modificar(self):
        if (self.interfaz.modificar_paciente.text()=="Modificar paciente"):
            self.interfaz.modificar_paciente.setText("Actualizar")
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setEnabled(True)
            self.lineEdit_3.setEnabled(True)
        else:
            paciente=self.lineEdit.text()
            edad=self.lineEdit_2.text()
            gravedad=self.lineEdit_3.text()
    # Función conectada al boton para realizarle la prueba al paciente
    # Nos abrirá la ventana con la que cronometramos el tiempo que el paciente
    # Tardará en realizar el recorrido
    def RealizarPrueba(self):
        CronoV2.MainWindow.paciente=self.interfaz.combo_pacientes.currentText()
        CronoV2.MainWindow().show()
    # Funcion conectada con el combo box
    # Nos comprobará si hay algún paciente seleccionado y cuando sea el caso
    # Nos habilitará los botones y llamará a la función que nos
    # Mostrará los datos del paciente
    def enableButtons(self):
        if (self.interfaz.combo_pacientes.currentText()=="Seleccionar paciente"):
            self.interfaz.modificar_paciente.setEnabled(False)
            self.interfaz.prueba_crono.setEnabled(False)
            self.interfaz.eliminar_paciente.setEnabled(False)
            self.lineEdit.setText=""
            self.lineEdit_2.setText=""
            self.lineEdit_3.setText=""
        else:
            self.interfaz.modificar_paciente.setEnabled(True)
            self.interfaz.prueba_crono.setEnabled(True)
            self.interfaz.eliminar_paciente.setEnabled(True)
            self.datosPaciente()
    # Funcion conectada con el boton de añadir paciente
    # 
    def BotonAddPaciente(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("I have a question!")
        dlg.setText("This is a simple dialog")
        button = dlg.exec_()
        if button == QMessageBox.Ok:
            print("OK!")
    # Funcion conectada con la función del combo box
    # Llamará a la función de la base de datos que nos
    # Dará los datos del paciente y la gráfica con los datos
    # Del paciente añadido.
    def datosPaciente(self):
        self.sc=self.BDatos.sql_MostrarGrafica(self.sc)
        datos=self.BDatos.sql_getDatosPacientes(self.interfaz.combo_pacientes.currentText())
        self.lineEdit.setText(datos[0][0])
        self.lineEdit_2.setText(str(datos[2][0]))
        self.lineEdit_3.setText(str(datos[1][0]))