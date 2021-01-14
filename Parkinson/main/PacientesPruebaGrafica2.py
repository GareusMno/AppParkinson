import sys
import sqlite3
import hashlib
import os

from PyQt5 import uic
import pathlib
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication,QListWidgetItem,QFrame,QListWidget,QDialog,QMessageBox,QLineEdit
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from pathlib import Path

import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from main import BD,Pacientes,PacientesPruebaGrafica2,addUser
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
        self.listaPacientes()
        #Conectamos los botones con su respectiva funcion
        self.interfaz.pruebaCrono.pressed.connect(self.RealizarPrueba)
        self.interfaz.addPaciente.pressed.connect(self.BotonaddPaciente)
        self.interfaz.modificarPaciente.pressed.connect(self.Modificar)
        self.interfaz.eliminarPaciente.pressed.connect(self.Eliminar)
        self.interfaz.editarClasificacion.pressed.connect(self.editar)
        #Creamos la capa de la grafica y activamos la opción de actualizar para que cuando
        #Cambiemos entre pacientes podamos actualizar sus datos
        self.graphWidget = pg.GraphicsWindow()
        self.num = 0
        #Se ha implementado de forma manual, así que la añadimos al layout y mostramos la interfaz
        self.interfaz.verticalLayout.addWidget(self.graphWidget)
        self.interfaz.show()
    # Función conectada la botón de modificar
    # Nos habilitará los campos del paciente para que podamos modificarlo
    # Además el mismo botón cambiará de nombre y nos servira para que una vez tengamos los campos
    # Como queremos los guardemos y actualizará la base de datos
    def Modificar(self):
        if (self.interfaz.modificarPaciente.text()=="Modificar paciente"):
            self.interfaz.modificarPaciente.setText("Actualizar")
            self.lePaciente.setEnabled(True)
            self.sbEdad.setEnabled(True)
            self.leGravedad.setEnabled(True)
            self.comboPacientes.setEnabled(False)
            self.listaPacientes()
        else:
            self.interfaz.modificarPaciente.setText("Modificar paciente")
            paciente=self.lePaciente.text()
            edad=self.sbEdad.text()
            gravedad=self.leGravedad.text()

            self.comboPacientes.setEnabled(False)
            self.lePaciente.setEnabled(False)
            self.sbEdad.setEnabled(False)
            self.leGravedad.setEnabled(True)

            self.addUserDialog = addUser.ModificarPaciente(paciente,edad)
            self.addUserDialog.show()
            self.addUserDialog.exec_()
    def Eliminar(self):
        nombre = self.interfaz.comboPacientes.currentText()
        self.addUserDialog = addUser.EliminarPaciente(nombre)
        self.addUserDialog.show()
        self.addUserDialog.exec_()
        self.listaPacientes()
    def editar(self):
        self.addUserDialog = addUser.ClasificacionPaciente()
        self.addUserDialog.show()
        self.addUserDialog.exec_()
    # Función conectada al boton para realizarle la prueba al paciente
    # Nos abrirá la ventana con la que cronometramos el tiempo que el paciente
    # Tardará en realizar el recorrido
    def RealizarPrueba(self):
        CronoV2.MainWindow.paciente=self.interfaz.comboPacientes.currentText()
        CronoV2.MainWindow().show()
    # Funcion conectada con el combo box
    # Nos comprobará si hay algún paciente seleccionado y cuando sea el caso
    # Nos habilitará los botones y llamará a la función que nos
    # Mostrará los datos del paciente
    def enableButtons(self):
        if (self.interfaz.comboPacientes.currentText()=="Seleccionar paciente"):
            self.interfaz.modificarPaciente.setEnabled(False)
            self.interfaz.pruebaCrono.setEnabled(False)
            self.interfaz.eliminarPaciente.setEnabled(False)
            self.lePaciente.setText("")
            self.sbEdad.setValue(0)
            self.leGravedad.setText("")
            if (BD.comprobado==1):
                self.graphWidget.removeItem(BD.lienzo)
            BD.comprobado=0
        else:
            if (BD.comprobado==1):
                self.graphWidget.removeItem(BD.lienzo)
            self.interfaz.modificarPaciente.setEnabled(True)
            self.interfaz.pruebaCrono.setEnabled(True)
            self.interfaz.eliminarPaciente.setEnabled(True)
            self.datosPaciente()
    # Funcion conectada con el boton de añadir paciente
    # 
    def BotonaddPaciente(self):
        self.addUserDialog = addUser.addPaciente()
        self.addUserDialog.show()
        self.addUserDialog.exec_()
        self.listaPacientes()
    # Funcion conectada con la función del combo box
    # Llamará a la función de la base de datos que nos
    # Dará los datos del paciente y la gráfica con los datos
    # Del paciente añadido.
    def datosPaciente(self):
        nombre=self.interfaz.comboPacientes.currentText()
        self.BDatos.sql_MostrarGrafica(self.graphWidget,nombre)
        datos=self.BDatos.sql_getDatosPacientes(nombre)
        self.lePaciente.setText(datos[0][0])
        self.leDNI.setText(datos[1][0])
        self.sbEdad.setValue(datos[2][0])
        self.leAltura.setText(datos[3][0])
        self.lePeso.setText(datos[4][0])
        self.leGravedad.setText(str(datos[5][0]))
    def listaPacientes(self):
        if (self.interfaz.comboPacientes.count()==1):
            self.interfaz.comboPacientes.clear()
            self.interfaz.comboPacientes.addItem("Seleccionar paciente")
            self.lista_pacientes=self.BDatos.sql_getPacientes()
            self.interfaz.comboPacientes.addItems(self.lista_pacientes)
            self.interfaz.comboPacientes.currentTextChanged.connect(self.enableButtons)