import sys
import os
import sqlite3
import hashlib
from pathlib import Path

from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

sys.path.append( '.' )
from main import BD
from main import Pacientes
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interfaz = uic.loadUi("ui/Login.ui")
        
        self.interfaz.Button.pressed.connect(self.CronoCod)
        self.interfaz.show()

    def CronoCod(self):
        b=self.interfaz.UserText.text()
        c=self.interfaz.PassText.text()
        BDatos = BD.Base()
        if os.path.isfile("bd/Parkinson.db"):
            if (BDatos.sql_ComprobarTabla("Usuarios")):
                if (BDatos.sql_ComprobarUsuario(b,c)):
                    self.hide()
                    Pacientes.MainWindow().show()
                else:
                    print("Datos incorrectos")
            else:
                BDatos.sql_CreateTable()
                if (BDatos.sql_ComprobarUsuario(b,c)):
                    self.hide()
                    exit()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    app.exec_()
