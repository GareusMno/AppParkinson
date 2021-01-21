import os
import sys

import sqlite3
import hashlib
import pathlib
from pathlib import Path
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication,QShortcut,QDialog,QLabel,QVBoxLayout,QMessageBox,QFileDialog
from PyQt5.QtGui import QKeySequence
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from main import BD,PacientesPruebaGrafica2,addUser
# Clase principal de la ventana de login
# Donde nos pedirán un usuario y una contraseña
# Para poder acceder a la aplicación
# Y en caso de no coincidir saltará una ventana informando del fallo
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #Instalará los programas necesarios para la ejecución del programa
        os.system("pip3 install -r "+".."+os.path.sep+"bin"+os.path.sep+"requirements.txt")

        #UI Cargada
        self.interfaz = uic.loadUi(".."+os.path.sep+"ui"+os.path.sep+"Login.ui")

        self.BDatos = BD.Base()

        #Comprobación de la existencia de la base de datos por defecto y creación
        #En caso de que no exista
        if os.path.isfile(".."+os.path.sep+"bd"+os.path.sep+"Parkinson.db"):
            if (self.BDatos.sql_ComprobarTabla()==False):
                self.BDatos.sql_CreateTable()
        self.interfaz.Button.pressed.connect(self.iniciar)
        self.interfaz.show()
        self.Basededades = "Parkinson.db"
        self.interfaz.actionImportar.triggered.connect(self.actionImportar)
        self.interfaz.actionSeleccionar.triggered.connect(self.usarBD)
    #
    #QAction que nos permitirá importar una base de datos, nos moverá la bd que seleccionemos
    #A nuestra carpeta de bd
    #
    def actionImportar(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file','.'+os.path.sep+'bd', 'DB files(*.db)')
        path = filename[0]
        nomF = path.split("/")  
        os.system("cp "+ path + " .."+os.path.sep+"bd"+os.path.sep+nomF[len(nomF)-1])     
    #
    #Función para cambiar la base de datos usada
    #La base de datos que seleccionemos cojerá el nombre de la bd y usaremos
    #La seleccionada en todas las operaciones
    #
    def usarBD(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file','.'+os.path.sep+'bd', 'DB files(*.db)')
        path = filename[0]
        nomF = path.split("/")
        self.Basededades = nomF[len(nomF)-1]
    #
    # Función para iniciar la siguiente ventana del programa una vez
    # Se haya introducido las datos correctos
    #
    def iniciar(self):
        b=self.interfaz.UserText.text()
        c=self.interfaz.PassText.text()
        if (self.BDatos.sql_ComprobarUsuario(b,c)):
            self.interfaz.close()
            # La primera vez de ejecución nos permitirá añadir un usuario extra
            if (self.BDatos.sql_ComprobarUsuarioDoctor()):
                self.addUserDialog = addUser.adUser()
                self.addUserDialog.show()
                self.addUserDialog.exec_()
            PacientesPruebaGrafica2.MainWindow(self.Basededades).show()
        else:
            dlg = QMessageBox(self)
            dlg.setIcon(QMessageBox.Information)
            dlg.setWindowTitle("Aviso!")
            dlg.setText("Usuario o contraseña incorrectos")
            dlg.exec_()
