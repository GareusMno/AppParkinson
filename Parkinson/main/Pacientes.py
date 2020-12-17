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

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BDatos = BD.Base()
        self.interfaz = uic.loadUi("ui/Pacientes.ui", self)
        self.lista_pacientes=self.BDatos.sql_getPacientes()
        self.interfaz.combo_pacientes.addItems(self.lista_pacientes)
        self.interfaz.combo_pacientes.currentTextChanged.connect(self.enableButtons)
        self.interfaz.prueba_crono.pressed.connect(self.RealizarPrueba)
        self.interfaz.AddPaciente.pressed.connect(self.BotonAddPaciente)
        self.sc = MplCanvas(self, width=10, height=4, dpi=100)
        self.sc.setUpdatesEnabled(True)
        self.interfaz.verticalLayout.addWidget(self.sc)
        self.interfaz.show()

    def RealizarPrueba(self):
        CronoV2.MainWindow.paciente=self.interfaz.combo_pacientes.currentText()
        CronoV2.MainWindow().show()
    def enableButtons(self):
        if (self.interfaz.combo_pacientes.currentText()=="Seleccionar paciente"):
            self.interfaz.modificar_paciente.setEnabled(False)
            self.interfaz.prueba_crono.setEnabled(False)
            self.interfaz.eliminar_paciente.setEnabled(False)
        else:
            self.interfaz.modificar_paciente.setEnabled(True)
            self.interfaz.prueba_crono.setEnabled(True)
            self.interfaz.eliminar_paciente.setEnabled(True)
            self.datosPaciente()
    def BotonAddPaciente(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("I have a question!")
        dlg.setText("This is a simple dialog")
        button = dlg.exec_()
        if button == QMessageBox.Ok:
            print("OK!")
    def datosPaciente(self):
        self.sc=self.BDatos.sql_MostrarGrafica(self.sc)
        datos=self.BDatos.sql_getDatosPacientes(self.interfaz.combo_pacientes.currentText())
        self.lineEdit.setText(datos[0][0])
        self.lineEdit_2.setText(str(datos[2][0]))
        self.lineEdit_3.setText(str(datos[1][0]))