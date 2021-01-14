import sys
import os
import sqlite3
import hashlib
import pathlib
from pathlib import Path
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication,QShortcut,QDialog,QLabel,QVBoxLayout,QMessageBox
from PyQt5.QtGui import QKeySequence
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from main import BD,Pacientes,PacientesPruebaGrafica2,addUser
# Clase principal de la ventana de login
# Donde nos pedirán un usuario y una contraseña
# Para poder acceder a la aplicación
# Y en caso de no coincidir saltará una ventana informando del fallo
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        p = QProcess()
        p.start("pip3 install -r requirements.txt")
        self.interfaz = uic.loadUi("ui/Login.ui")
        self.BDatos = BD.Base()
        if os.path.isfile("bd/Parkinson.db"):
            if (self.BDatos.sql_ComprobarTabla()==False):
                self.BDatos.sql_CreateTable()
        self.interfaz.Button.pressed.connect(self.iniciar)
        self.interfaz.show()
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
