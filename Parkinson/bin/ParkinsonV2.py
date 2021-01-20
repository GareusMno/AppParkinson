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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.system("pip3 install -r "+"."+os.path.sep+"bin"+os.path.sep+"requirements.txt")
        self.interfaz = uic.loadUi("."+os.path.sep+"ui"+os.path.sep+"Login.ui")
        self.BDatos = BD.Base()
        if os.path.isfile("."+os.path.sep+"bd"+os.path.sep+"Parkinson.db"):
            if (self.BDatos.sql_ComprobarTabla()==False):
                self.BDatos.sql_CreateTable()
        self.interfaz.Button.pressed.connect(self.iniciar)
        self.interfaz.show()
        self.Basededades = "Parkinson.db"
        self.interfaz.actionImportar.triggered.connect(self.actionImportar)
        #self.interfaz.actionExportar.triggered.connect(self.actionExportar)
        self.interfaz.actionSeleccionar.triggered.connect(self.usarBD)
   
    def actionImportar(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file','.'+os.path.sep+'bd', 'DB files(*.db)')
        path = filename[0]
        nomF = path.split("/")  
        os.system("cp "+ path + " .."+os.path.sep+"bd"+os.path.sep+nomF[len(nomF)-1])     
    def usarBD(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file','.'+os.path.sep+'bd', 'DB files(*.db)')
        path = filename[0]
        nomF = path.split("/")
        self.Basededades = nomF[len(nomF)-1]
    def iniciar(self):
        b=self.interfaz.UserText.text()
        c=self.interfaz.PassText.text()
        if (self.BDatos.sql_ComprobarUsuario(b,c)):
            self.interfaz.close()
            if (self.BDatos.sql_ComprobarUsuarioDoctor()):
                self.addUserDialog = addUser.addUser()
                self.addUserDialog.show()
                self.addUserDialog.exec_()
            PacientesPruebaGrafica2.MainWindow().show()
        else:
            dlg = QMessageBox(self)
            dlg.setIcon(QMessageBox.Information)
            dlg.setWindowTitle("Aviso!")
            dlg.setText("Usuario o contraseña incorrectos")
            dlg.exec_()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    app.exec_()
