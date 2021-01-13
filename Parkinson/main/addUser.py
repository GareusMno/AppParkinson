import sys
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

sys.path.append( '.' )
from main import BD

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
        self.ledad = QLabel("Edad:")
        self.sedad = QSpinBox()
        self.lgravedad = QLabel("Gravedad:")
        self.egravedad = QLineEdit()
        ldatos.addRow(self.lnombre,self.enombre)
        ldatos.addRow(self.ledad,self.sedad)
        ldatos.addRow(self.lgravedad,self.egravedad)
        vBox = QVBoxLayout()
        vBox.addWidget(bTrue)
        vBox.addWidget(self.lInvalidUser)
        lprincipal.addLayout(ldatos)
        lprincipal.addLayout(vBox)
        self.setLayout(lprincipal)

    def bTrueClicked(self):
        # Si cliquem el botó considerem l'usuari vàlid i tanquem el dialeg
        nombre = self.enombre.text()
        edad = self.sedad.text()
        gravedad = self.egravedad.text()
        print(nombre)
        print(edad)
        print(gravedad)
        self.BDatos.sql_InsertarPaciente(nombre,edad,gravedad)
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

