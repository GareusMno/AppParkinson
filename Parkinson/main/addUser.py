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
    QSpinBox,
    QComboBox,
    QDoubleSpinBox,
    QDateTimeEdit
)

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from main import BD,PacientesPruebaGrafica2,addUser

class addPaciente(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Añadir paciente")
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.BDatos = BD.Base()

        bFalse = QPushButton("Cancelar")
        bFalse.clicked.connect(self.bFalseClicked)

        bTrue = QPushButton("Confirmar")
        bTrue.clicked.connect(self.bTrueClicked)
        
        lprincipal = QVBoxLayout()
        ldatos = QFormLayout()
        self.lnombre = QLabel()
        self.lnombre.setText("Nombre:")
        self.lenombre = QLineEdit()

        self.lapellido = QLabel()
        self.lapellido.setText("Apellido:")
        self.leapellido = QLineEdit()

        self.ldir = QLabel()
        self.ldir.setText("Direccion:")
        self.ledir = QLineEdit()

        self.lemail = QLabel()
        self.lemail.setText("Email:")
        self.leemail = QLineEdit()

        self.ltelefono = QLabel()
        self.ltelefono.setText("Teléfono:")
        self.letelefono = QLineEdit()

        self.lsip = QLabel()
        self.lsip.setText("SIP:")
        self.lesip = QLineEdit()

        self.lgenero = QLabel()
        self.lgenero.setText("Genero:")

        self.legenero = QComboBox()
        self.legenero.addItem("Seleccionar género")
        self.legenero.addItem("Masculino")
        self.legenero.addItem("Femenino")
        self.legenero.addItem("Otro")

        self.lestadio = QLabel()
        self.lestadio.setText("Estadio:")

        self.cbestadio = QComboBox()
        self.cbestadio.addItem("Seleccionar estadio")
        self.cbestadio.addItem("Estadio 0")
        self.cbestadio.addItem("Estadio 1")
        self.cbestadio.addItem("Estadio 2")
        self.cbestadio.addItem("Estadio 3")
        self.cbestadio.addItem("Estadio 4")
        self.cbestadio.addItem("Estadio 5")

        self.ledad = QLabel()
        self.ledad.setText("Nacimiento:")
        self.leedad = QDateTimeEdit()

        self.limc = QLabel()
        self.limc.setText("IMC:")
        self.leimc = QSpinBox()
        self.leimc.setMaximum(1000)

        self.lgrasa = QLabel()
        self.lgrasa.setText("Grasa corporal:")
        self.legrasa = QSpinBox()
        self.legrasa.setMaximum(1000)

        self.laltura = QLabel()
        self.laltura.setText("Altura:")
        self.lealtura = QSpinBox()
        self.lealtura.setMaximum(1000)

        self.lpeso = QLabel()
        self.lpeso.setText("Peso:")
        self.lepeso = QSpinBox()
        self.lepeso.setMaximum(1000)

        self.ldni = QLabel()
        self.ldni.setText("DNI:")
        self.ledni = QLineEdit()

        ldatos.addRow(self.lnombre,self.lenombre)
        ldatos.addRow(self.lapellido,self.leapellido)
        ldatos.addRow(self.lsip,self.lesip)
        ldatos.addRow(self.ldni,self.ledni)
        ldatos.addRow(self.ldir,self.ledir)
        ldatos.addRow(self.lemail,self.leemail)
        ldatos.addRow(self.lestadio,self.cbestadio)
        ldatos.addRow(self.ltelefono,self.letelefono)
        ldatos.addRow(self.lgenero,self.legenero)
        ldatos.addRow(self.ledad,self.leedad)
        ldatos.addRow(self.limc,self.leimc)
        ldatos.addRow(self.lgrasa,self.legrasa)
        ldatos.addRow(self.laltura,self.lealtura)
        ldatos.addRow(self.lpeso,self.lepeso)
        
        vBox = QVBoxLayout()
        vBox.addWidget(bFalse)
        vBox.addWidget(bTrue)
        lprincipal.addLayout(ldatos)
        lprincipal.addLayout(vBox)
        self.setLayout(lprincipal)
    def bTrueClicked(self):
        # Si cliquem el botó considerem l'usuari vàlid i tanquem el dialeg
        nombre = str(self.lenombre.text())
        apellido = str(self.leapellido.text())
        dni = str(self.ledni.text())
        direccion = str(self.ledir.text())
        correo = str(self.leemail.text())
        telefono = str(self.letelefono.text())
        genero = str(self.legenero.currentText())
        sip = str(self.lesip.text())
        edad = str(self.leedad.dateTime().toString())
        IMC = str(self.leimc.value())
        grasacorporal = str(self.legrasa.value())
        altura = str(self.lealtura.value())
        peso = str(self.lepeso.value())
        estadio = str(self.cbestadio.currentText())
        self.BDatos.sql_InsertarPaciente(nombre,apellido,altura,peso,dni,direccion,correo,telefono,sip,edad,genero,IMC,grasacorporal,estadio)
        self.close()
    def bFalseClicked(self):
        # No guardem
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
    def __init__(self,noriginal,nombre,apellido,sip,medicacion,estadio):
        super().__init__()
        self.paciente=noriginal
        self.nom=nombre
        self.ape=apellido
        self.SI= sip
        self.med = medicacion
        self.est= estadio
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
        self.BDatos.sql_ActualizarPaciente(self.paciente,self.nom,self.ape,self.SI,self.med,self.est)
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
        self.BDatos.sql_ActualizarClasificacion(self.lemin1.text(),self.lemax1.text(),self.lemin2.text(),self.lemax2.text(),self.lemin3.text(),self.lemax3.text(),self.lemin4.text(),self.lemax4.text())
        self.close()
    def bFalseClicked(self):
        # No guardem
        self.close()
class GuardarPrueba(QDialog):
    def __init__(self,total,s1,s2,s3):
        super().__init__()
        self.setWindowTitle("Guardar prueba")
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)

        bTrue = QPushButton("Confirmar")
        bTrue.clicked.connect(self.bTrueClicked)
        
        lprincipal = QVBoxLayout()
        ldatos = QFormLayout()
        self.ltotal = QLabel()
        self.ltotal.setText("Total:")
        self.letotal = QLineEdit()
        self.letotal.setEnabled(False)
        self.letotal.setText(total)

        self.ls1 = QLabel()
        self.ls1.setText("Segmento 1:")
        self.les1 = QLineEdit()
        self.les1.setEnabled(False)
        self.les1.setText(s1)

        self.ls2 = QLabel()
        self.ls2.setText("Segmento 2:")
        self.les2 = QLineEdit()
        self.les2.setEnabled(False)
        self.les2.setText(s2)

        self.ls3 = QLabel()
        self.ls3.setText("Segmento 3:")
        self.les3 = QLineEdit()
        self.les3.setEnabled(False)
        self.les3.setText(s3)

        self.confirmacion = QLabel()
        self.confirmacion.setText("Prueba guardada!")
        ldatos.addRow(self.ls1,self.les1)
        ldatos.addRow(self.ls2,self.les2)
        ldatos.addRow(self.ls3,self.les3)
        ldatos.addRow(self.ltotal,self.letotal)
        ldatos.addRow(self.confirmacion)
        vBox = QVBoxLayout()
        vBox.addWidget(bTrue)
        lprincipal.addLayout(ldatos)
        lprincipal.addLayout(vBox)
        self.setLayout(lprincipal)
    def bTrueClicked(self):
        # Si cliquem el botó considerem l'usuari vàlid i tanquem el dialeg
        self.close()
class ExtraPaciente(QDialog):
    def __init__(self,nombre):
        super().__init__()
        self.BDatos = BD.Base()
        self.nom = nombre
        datos=self.BDatos.sql_getExtra(nombre)
        self.direccion=str(datos[0][0])
        self.email=str(datos[1][0])
        self.telefono=str(datos[2][0])
        self.genero=str(datos[3][0])
        self.fechaingreso=str(datos[4][0])
        self.imc=str(datos[5][0])
        self.grasacorporal=str(datos[6][0])
        self.altura=str(datos[7][0])
        self.peso=str(datos[8][0])
        self.dni=str(datos[9][0])
        self.setWindowTitle("Informacion extra")
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)

        bFalse = QPushButton("Cancelar")
        bFalse.clicked.connect(self.bFalseClicked)

        bTrue = QPushButton("Confirmar")
        bTrue.clicked.connect(self.bTrueClicked)
        
        lprincipal = QVBoxLayout()
        ldatos = QFormLayout()
        self.ldir = QLabel()
        self.ldir.setText("Direccion:")
        self.ledir = QLineEdit()
        self.ledir.setText(self.direccion)

        self.lemail = QLabel()
        self.lemail.setText("Email:")
        self.leemail = QLineEdit()
        self.leemail.setText(self.email)

        self.ltelefono = QLabel()
        self.ltelefono.setText("Teléfono:")
        self.letelefono = QLineEdit()
        self.letelefono.setText(self.telefono)

        self.lgenero = QLabel()
        self.lgenero.setText("Genero:")
        self.legenero = QLineEdit()
        self.legenero.setText(self.genero)

        self.lfecha = QLabel()
        self.lfecha.setText("Fecha ingresado:")
        self.lefecha = QLineEdit()
        self.lefecha.setEnabled(False)
        self.lefecha.setText(self.fechaingreso)

        self.limc = QLabel()
        self.limc.setText("IMC:")
        self.leimc = QLineEdit()
        self.leimc.setText(self.imc)

        self.lgrasa = QLabel()
        self.lgrasa.setText("Grasa corporal:")
        self.legrasa = QLineEdit()
        self.legrasa.setText(self.grasacorporal)

        self.laltura = QLabel()
        self.laltura.setText("Altura:")
        self.lealtura = QLineEdit()
        self.lealtura.setText(self.altura)

        self.lpeso = QLabel()
        self.lpeso.setText("Peso:")
        self.lepeso = QLineEdit()
        self.lepeso.setText(self.peso)

        self.ldni = QLabel()
        self.ldni.setText("DNI:")
        self.ledni = QLineEdit()
        self.ledni.setText(self.dni)

        ldatos.addRow(self.ldni,self.ledni)
        ldatos.addRow(self.ldir,self.ledir)
        ldatos.addRow(self.lemail,self.leemail)
        ldatos.addRow(self.ltelefono,self.letelefono)
        ldatos.addRow(self.lgenero,self.legenero)
        ldatos.addRow(self.lfecha,self.lefecha)
        ldatos.addRow(self.limc,self.leimc)
        ldatos.addRow(self.lgrasa,self.legrasa)
        ldatos.addRow(self.laltura,self.lealtura)
        ldatos.addRow(self.lpeso,self.lepeso)
        
        vBox = QVBoxLayout()
        vBox.addWidget(bFalse)
        vBox.addWidget(bTrue)
        lprincipal.addLayout(ldatos)
        lprincipal.addLayout(vBox)
        self.setLayout(lprincipal)
    def bTrueClicked(self):
        # Si cliquem el botó considerem l'usuari vàlid i tanquem el dialeg
        dni = str(self.ledni.text())
        direccion = str(self.ledir.text())
        correo = str(self.leemail.text())
        telefono = str(self.letelefono.text())
        genero = str(self.legenero.text())
        IMC = str(self.leimc.text())
        grasacorporal = str(self.legrasa.text())
        altura = str(self.lealtura.text())
        peso = str(self.lepeso.text())

        self.BDatos.sql_ActualizarExtraPaciente(self.nom,dni,direccion,correo,telefono,genero,IMC,grasacorporal,altura,peso)
        self.close()
    def bFalseClicked(self):
        # No guardem
        self.close()
