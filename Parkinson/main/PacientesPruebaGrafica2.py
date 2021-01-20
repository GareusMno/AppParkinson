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
from main import BD,PacientesPruebaGrafica2,addUser,CronoV2
# Clase principal de la ventana de los pacientes
# Que nos mostrara una lista de cada paciente y segun el paciente
# Seleccionado nos mostrará sus datos y una gráfica con sus tiempos
class MainWindow(QMainWindow):
    def __init__(self,bd):
        super().__init__()
        # Cargamos la interfaz creada con QTDesigner 
        self.BDActual = bd
        self.interfaz = uic.loadUi(".."+os.path.sep+"ui"+os.path.sep+"Pacientes.ui", self)
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
        self.interfaz.extraPaciente.pressed.connect(self.infoExtra)
        self.interfaz.actualizarGrafica.pressed.connect(self.datosPaciente)
        #Creamos la capa de la grafica y activamos la opción de actualizar para que cuando
        #Cambiemos entre pacientes podamos actualizar sus datos
        #self.graphWidget = pg.GraphicsWindow()
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground(None)
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
            self.leNombre.setEnabled(True)
            self.leApellido.setEnabled(True)
            self.leSIP.setEnabled(True)
            self.teMedicacion.setEnabled(True)
            self.comboPacientes.setEnabled(False)

            self.interfaz.addPaciente.setEnabled(False)
            self.interfaz.eliminarPaciente.setEnabled(False)
            self.interfaz.extraPaciente.setEnabled(False)
            self.interfaz.pruebaCrono.setEnabled(False)
            self.interfaz.editarClasificacion.setEnabled(False)
            self.interfaz.actualizarGrafica.setEnabled(False)
        else:
            self.interfaz.modificarPaciente.setText("Modificar paciente")
            paciente=self.leNombre.text()
            self.comboPacientes.setEnabled(True)
            self.interfaz.eliminarPaciente.setEnabled(True)
            self.interfaz.extraPaciente.setEnabled(True)
            self.interfaz.pruebaCrono.setEnabled(True)
            self.interfaz.addPaciente.setEnabled(True)
            self.interfaz.editarClasificacion.setEnabled(True)
            self.interfaz.actualizarGrafica.setEnabled(True)
            self.leNombre.setEnabled(False)
            self.leApellido.setEnabled(False)
            self.leSIP.setEnabled(False)
            self.teMedicacion.setEnabled(False)
            nombre = self.interfaz.comboPacientes.currentText()
            self.addUserDialog = addUser.ModificarPaciente(nombre,self.leNombre.text(),self.leApellido.text(),self.leSIP.text(),self.teMedicacion.toPlainText())
            self.addUserDialog.show()
            self.addUserDialog.exec_()
            self.listaPacientes()
    #
    #Función para eliminar al paciente seleccionado y actualiza la lista
    #
    def Eliminar(self):
        nombre = self.interfaz.comboPacientes.currentText()
        self.addUserDialog = addUser.EliminarPaciente(nombre)
        self.addUserDialog.show()
        self.addUserDialog.exec_()
        self.listaPacientes()
    #
    #Función para abrir la ventana de la clasificación de los pacientes
    #
    def editar(self):
        self.addUserDialog = addUser.ClasificacionPaciente()
        self.addUserDialog.show()
        self.addUserDialog.exec_()
    # Función conectada al boton para realizarle la prueba al paciente
    # Nos abrirá la ventana con la que cronometramos el tiempo que el paciente
    # Tardará en realizar el recorrido
    def RealizarPrueba(self):
        CronoV2.MainWindow.paciente=self.interfaz.comboPacientes.currentText()
        self.añadirPrueba = CronoV2.MainWindow(self.BDActual)
        self.añadirPrueba.show()
        self.datosPaciente()
    # Funcion conectada con el combo box
    # Nos comprobará si hay algún paciente seleccionado y cuando sea el caso
    # Nos habilitará los botones y llamará a la función que nos
    # Mostrará los datos del paciente
    def enableButtons(self):
        if (self.interfaz.comboPacientes.currentText()=="Seleccionar paciente"):
            self.interfaz.modificarPaciente.setEnabled(False)
            self.interfaz.pruebaCrono.setEnabled(False)
            self.interfaz.eliminarPaciente.setEnabled(False)
            self.interfaz.extraPaciente.setEnabled(False)
            self.interfaz.actualizarGrafica.setEnabled(False)
            self.leNombre.setText("")
            self.leApellido.setText("")
            self.leSIP.setText("")
            self.leIngresado.setText("")
            self.leGravedad.setText("")
            self.teMedicacion.setText("")
            if (BD.comprobado==1):
                self.graphWidget.clear()
            BD.comprobado=0
        else:
            if (BD.comprobado==1):
                self.graphWidget.clear()
            self.interfaz.modificarPaciente.setEnabled(True)
            self.interfaz.pruebaCrono.setEnabled(True)
            self.interfaz.eliminarPaciente.setEnabled(True)
            self.interfaz.extraPaciente.setEnabled(True)
            self.interfaz.actualizarGrafica.setEnabled(True)
            self.datosPaciente()
    #
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
        self.leNombre.setText(str(datos[0][0]))
        self.leApellido.setText(str(datos[1][0]))
        self.leSIP.setText(str(datos[2][0]))
        self.leIngresado.setText(str(datos[3][0]))
        self.leGravedad.setText(str(datos[4][0]))
        self.teMedicacion.setText(str(datos[5][0]))
    #
    #Función que llenará los campos de la combobox con los nombres de los pacientes
    #
    def listaPacientes(self):
        self.interfaz.comboPacientes.clear()
        self.interfaz.comboPacientes.addItem("Seleccionar paciente")
        self.lista_pacientes=self.BDatos.sql_getPacientes()
        self.interfaz.comboPacientes.addItems(self.lista_pacientes)
        self.interfaz.comboPacientes.currentTextChanged.connect(self.enableButtons)
    #
    # Función que nos mostrará una ventana con los datos extra del paciente que no son
    # mostrados en la ventana principal
    #
    def infoExtra(self):
        nombre = self.interfaz.comboPacientes.currentText()
        self.addUserDialog = addUser.ExtraPaciente(nombre)
        self.addUserDialog.show()
        self.addUserDialog.exec_()