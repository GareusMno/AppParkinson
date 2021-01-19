import sys
import os

import pathlib
from pathlib import Path
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFormLayout,
    QLineEdit,
    QSpinBox
)

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from main import BD,PacientesPruebaGrafica2,addUser

class addPaciente(QDialog):
    def __init__(self):
        super().__init__()
        self.BDatos = BD.Base()
        self.setWindowTitle("Añadir paciente")
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)

        bTrue = QPushButton("Guardar")

        bTrue.clicked.connect(self.bTrueClicked)

        self.lInvalidUser = QLabel("Usuari o contrasenya incorrectes")
        self.lInvalidUser.setStyleSheet("QLabel{ color: red }")
        self.lInvalidUser.setVisible(False)
        lprincipal = QVBoxLayout()
        ldatos = QFormLayout()
        self.lnombre = QLabel("Nombre:")
        self.enombre = QLineEdit()
        self.ldni = QLabel("DNI:")
        self.edni = QLineEdit()
        self.ledad = QLabel("Edad:")
        self.sedad = QSpinBox()
        self.laltura = QLabel("Altura:")
        self.ealtura = QLineEdit()
        self.lpeso = QLabel("Peso:")
        self.epeso = QLineEdit()
        ldatos.addRow(self.lnombre,self.enombre)
        ldatos.addRow(self.ldni,self.edni)
        ldatos.addRow(self.ledad,self.sedad)
        ldatos.addRow(self.laltura,self.ealtura)
        ldatos.addRow(self.lpeso,self.epeso)
        vBox = QVBoxLayout()
        vBox.addWidget(bTrue)
        vBox.addWidget(self.lInvalidUser)
        lprincipal.addLayout(ldatos)
        lprincipal.addLayout(vBox)
        self.setLayout(lprincipal)

    def bTrueClicked(self):
        # Si cliquem el botó considerem l'usuari vàlid i tanquem el dialeg
        nombre = str(self.enombre.text())
        edad = str(self.sedad.text())
        dni = str(self.edni.text())
        peso = str(self.epeso.text())
        altura = str(self.ealtura.text())
        self.BDatos.sql_InsertarPaciente(nombre,edad,dni,peso,altura)
        self.close()

class addUser(QDialog):
    def __init__(self):
        super().__init__()
        self.BDatos = BD.Base()
        self.setWindowTitle("Añadir usuario")
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)

        bTrue = QPushButton("Guardar")

        bTrue.clicked.connect(self.bTrueClicked)

        self.lInvalidUser = QLabel("Usuari o contrasenya incorrectes")
        self.lInvalidUser.setStyleSheet("QLabel{ color: red }")
        self.lInvalidUser.setVisible(False)
        lprincipal = QVBoxLayout()
        ldatos = QFormLayout()
        self.lnombre = QLabel("Nombre:")
        self.enombre = QLineEdit()
        self.lcontraseña = QLabel("Contraseña:")
        self.econtraseña = QLineEdit()
        self.econtraseña.setEchoMode(QLineEdit.Password)
        ldatos.addRow(self.lnombre,self.enombre)
        ldatos.addRow(self.lcontraseña,self.econtraseña)
        vBox = QVBoxLayout()
        vBox.addWidget(bTrue)
        vBox.addWidget(self.lInvalidUser)
        lprincipal.addLayout(ldatos)
        lprincipal.addLayout(vBox)
        self.setLayout(lprincipal)

    def bTrueClicked(self):
        # Si cliquem el botó considerem l'usuari vàlid i tanquem el dialeg
        nombre = self.enombre.text()
        contraseña = self.econtraseña.text()
        print(nombre)
        print(contraseña)
        self.BDatos.sql_InsertarUsuario(nombre,contraseña)
        self.close()
class EliminarPaciente(QDialog):
    def __init__(self,nombre):
        super().__init__()
        self.paciente=nombre
        self.BDatos = BD.Base()
        self.setWindowTitle("Eliminar paciente")
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)

        bFalse = QPushButton("Cancelar")
        bFalse.clicked.connect(self.bFalseClicked)

        bTrue = QPushButton("Confirmar")
        bTrue.clicked.connect(self.bTrueClicked)
        
        lprincipal = QVBoxLayout()
        ldatos = QFormLayout()
        self.lnombre = QLabel("¿Seguro que quiere eliminar al paciente "+self.paciente+"?")
        ldatos.addRow(self.lnombre)
        vBox = QVBoxLayout()
        vBox.addWidget(bFalse)
        vBox.addWidget(bTrue)
        lprincipal.addLayout(ldatos)
        lprincipal.addLayout(vBox)
        self.setLayout(lprincipal)

    def bTrueClicked(self):
        # Si cliquem el botó considerem l'usuari vàlid i tanquem el dialeg
        self.BDatos.sql_EliminarPaciente(self.paciente)
        self.close()
    def bFalseClicked(self):
        # No guardem
        self.close()
class ModificarPaciente(QDialog):
    def __init__(self,nombre,edad):
        super().__init__()
        self.paciente=nombre
        self.edad=edad
        self.BDatos = BD.Base()
        self.setWindowTitle("Modificar paciente")
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)

        bFalse = QPushButton("Cancelar")
        bFalse.clicked.connect(self.bFalseClicked)

        bTrue = QPushButton("Confirmar")
        bTrue.clicked.connect(self.bTrueClicked)
        
        lprincipal = QVBoxLayout()
        ldatos = QFormLayout()
        self.lnombre = QLabel("¿Seguro que quiere modificar el paciente "+self.paciente+"?")
        ldatos.addRow(self.lnombre)
        vBox = QVBoxLayout()
        vBox.addWidget(bFalse)
        vBox.addWidget(bTrue)
        lprincipal.addLayout(ldatos)
        lprincipal.addLayout(vBox)
        self.setLayout(lprincipal)
    def bTrueClicked(self):
        # Si cliquem el botó considerem l'usuari vàlid i tanquem el dialeg
        self.BDatos.sql_ActualizarPaciente(self.paciente,self.edad)
        self.close()
    def bFalseClicked(self):
        # No guardem
        self.close()
class ClasificacionPaciente(QDialog):
    def __init__(self):
        super().__init__()
        self.BDatos = BD.Base()
        datos=self.BDatos.sql_getClasificacion()
        self.min1=str(datos[0][0])
        self.max1=str(datos[1][0])
        self.min2=str(datos[0][1])
        self.max2=str(datos[1][1])
        self.min3=str(datos[0][2])
        self.max3=str(datos[1][2])
        self.min4=str(datos[0][3])
        self.max4=str(datos[1][3])
        self.setWindowTitle("Clasificacion por vuelta")
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)

        bFalse = QPushButton("Cancelar")
        bFalse.clicked.connect(self.bFalseClicked)

        bTrue = QPushButton("Confirmar")
        bTrue.clicked.connect(self.bTrueClicked)
        
        lprincipal = QVBoxLayout()
        ldatos = QFormLayout()
        self.lemin1 = QLineEdit()
        self.lemin1.setText(self.min1)
        self.lemax1 = QLineEdit()
        self.lemax1.setText(self.max1)
        self.lemin2 = QLineEdit()
        self.lemin2.setText(self.min2)
        self.lemax2 = QLineEdit()
        self.lemax2.setText(self.max2)
        self.lemin3 = QLineEdit()
        self.lemin3.setText(self.min3)
        self.lemax3 = QLineEdit()
        self.lemax3.setText(self.max3)
        self.lemin4 = QLineEdit()
        self.lemin4.setText(self.min4)
        self.lemax4 = QLineEdit()
        self.lemax4.setText(self.max4)
        ldatos.addRow(self.lemin1,self.lemax1)
        ldatos.addRow(self.lemin2,self.lemax2)
        ldatos.addRow(self.lemin3,self.lemax3)
        ldatos.addRow(self.lemin4,self.lemax4)
        vBox = QVBoxLayout()
        vBox.addWidget(bFalse)
        vBox.addWidget(bTrue)
        lprincipal.addLayout(ldatos)
        lprincipal.addLayout(vBox)
        self.setLayout(lprincipal)
    def bTrueClicked(self):
        # Si cliquem el botó considerem l'usuari vàlid i tanquem el dialeg
        self.BDatos.sql_ActualizarPaciente(self.paciente,self.edad)
        self.close()
    def bFalseClicked(self):
        # No guardem
        self.close()
class GuardarPrueba(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modificar paciente")
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)

        bTrue = QPushButton("Confirmar")
        bTrue.clicked.connect(self.bTrueClicked)
        
        lprincipal = QVBoxLayout()
        ldatos = QFormLayout()
        self.confirmacion = QLabel()
        self.confirmacion.setText("Prueba guardada!")
        ldatos.addRow(self.confirmacion)
        vBox = QVBoxLayout()
        vBox.addWidget(bTrue)
        lprincipal.addLayout(ldatos)
        lprincipal.addLayout(vBox)
        self.setLayout(lprincipal)
    def bTrueClicked(self):
        # Si cliquem el botó considerem l'usuari vàlid i tanquem el dialeg
        self.close()




