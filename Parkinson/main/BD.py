import sqlite3
import hashlib
import os
import sys

from sqlite3 import Error
import pathlib
from pathlib import Path
from dateutil import parser
import matplotlib.pyplot as plt
import datetime
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from datetime import datetime
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from main import Cifrar

lienzo = 0
comprobado = 0
# Clase de la base de datos que al crearla y anos ofrecerá la conexion
# Con la base de datos y nos permitira acceder a todas las funciones
# Relacionadas con la base de datos
#class TimeAxisItem(pg.AxisItem):
#    def tickStrings(self, values, scale, spacing):
#        return [datetime.fromtimestamp(value) for value in values]
class Base(object):
    def __init__(self, nomDB = "Parkinson.db"):
        self.con=""
        try:
            
            self.con = sqlite3.connect(Path.joinpath(Path(__file__).parent.parent,"bd/"+nomDB))

        except Error:

            print(Error)
    # Función de crear tablas
    # Función que se ejecutará al principio y creará las tablas vacías
    # De la base de datos para que podamos trabajar con ellas
    # E insertara el usuario por defecto root con contraseña root
    def sql_CreateTable(self):
        cursorObj = self.con.cursor()

        cursorObj.execute("CREATE TABLE Usuarios(usuario String PRIMARY KEY not null default root, password String not null default root);")
        cursorObj.execute('INSERT INTO Usuarios(usuario, password) VALUES("root", "dc76e9f0c0006e8f919e0c515c66dbba3982f785");')
        cursorObj.execute("CREATE TABLE Pacientes(codigo INTEGER PRIMARY KEY AUTOINCREMENT, nombre String not null, "+
        "apellido String not null,direccion String, email String, Telefono String, SIP string, nacimiento String, genero String, fechaingreso String,"+
        "IMC String, grasacorporal String, altura String, peso String, DNI String not null, gravedad String, medicacion String);")
        cursorObj.execute("INSERT INTO Pacientes(nombre,apellido,altura,peso,DNI,direccion,email,Telefono,SIP,nacimiento,genero,fechaingreso,IMC,grasacorporal,medicacion) VALUES('Pepe','vivaldi',180,90,'ASDEQE3','asdasd','hola@gmail.com','812312123','asd31424','23/5/20','Masculino','Hoy','125','2153','Ibuprofreno 2 al dia');")
        cursorObj.execute("CREATE TABLE Pruebas(codigo INTEGER PRIMARY KEY AUTOINCREMENT, paciente String not null, lap1 INTEGER, lap2 INTEGER, lap3 INTEGER, TiempoTotal INTEGER ,fecha String, FOREIGN KEY(paciente) REFERENCES Pacientes(codigo) ON UPDATE CASCADE);")
        cursorObj.execute("CREATE TABLE Clasificacion(segmento INTEGER PRIMARY KEY AUTOINCREMENT,t1 INTEGER,t2 INTEGER);")
        cursorObj.execute("INSERT INTO Clasificacion(t1,t2) VALUES(17.16,23.56);")
        cursorObj.execute("INSERT INTO Clasificacion(t1,t2) VALUES(15.14,25.90);")
        cursorObj.execute("INSERT INTO Clasificacion(t1,t2) VALUES(10.43,13.34);")
        cursorObj.execute("INSERT INTO Clasificacion(t1,t2) VALUES(41.91,60.32);")
        self.con.commit()
    # Función de insertar pacientes
    # Se ejecutará cuando queramos añadir nuevos pacientes
    # Nos pasarán los datos de cada paciente por parámetros y le haremos un insert a la base de datos
    def sql_InsertarPaciente(self,nombre,apellido,altura,peso,DNI,direccion,email,Telefono,SIP,nacimiento,genero,imc,grasacorporal):
        cursorObj = self.con.cursor()
        cursorObj.execute("INSERT INTO Pacientes(nombre,apellido,altura,peso,DNI,direccion,email,Telefono,SIP,nacimiento,genero,fechaingreso,IMC,grasacorporal) "+
        "VALUES('"+nombre+"','"+apellido+"','"+altura+"','"+peso+"','"+DNI+"','"+direccion+"','"+email+"','"+Telefono+"','"+SIP+"','"+nacimiento+"','"+genero+"',datetime('now','localtime'),'"+imc+"','"+grasacorporal+"');")
        self.con.commit()
    # Función de eliminar pacientes
    # Se ejecutará cuando queramos eliminar un paciente
    # Le pasaran el nombre del paciente que se quiere eliminar
    # Y se ejecutará la sentencia SQL
    def sql_EliminarPaciente(self,paciente):
        cursorObj = self.con.cursor()
        cursorObj.execute('DELETE FROM Pacientes where nombre="'+paciente+'"')
        self.con.commit()
    # Función de actualizar pacientes
    # Se ejecutará cuando modifiquemos un paciente
    # Que hara un update según los datos actualizados que le serán pasados por parámetros
    def sql_ActualizarPaciente(self,noriginal,nombre,apellido,SIP,medicacion):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT codigo FROM Pacientes where nombre='"+noriginal+"'")
        codigos = cursorObj.fetchall()
        codigo = [_[0] for _ in codigos]
        print(codigo[0])
        cursorObj.execute("UPDATE Pacientes SET nombre='"+nombre+"',apellido='"+apellido+"',SIP='"+SIP+"',medicacion='"+medicacion+"' where codigo="+str(codigo[0])+";")
        self.con.commit()
    #
    #Función que actualizará la gravedad del paciente según el resultado de la prueba
    #
    def sql_ActualizarGravedad(self,paciente,gravedad):
        cursorObj = self.con.cursor()
        cursorObj.execute("UPDATE Pacientes SET gravedad='"+gravedad+"' where nombre='"+paciente+"';")
        self.con.commit()
    #
    #Función que actualizará la clasificación de las pruebas si las modificamos
    #
    def sql_ActualizarClasificacion(self,seg1a,seg1b,seg2a,seg2b,seg3a,seg3b,seg4a,seg4b):
        cursorObj = self.con.cursor()
        cursorObj.execute("UPDATE Clasificacion SET t1='"+seg1a+"',t2='"+seg1b+"' where segmento=1;")
        cursorObj.execute("UPDATE Clasificacion SET t1='"+seg2a+"',t2='"+seg2b+"' where segmento=2;")
        cursorObj.execute("UPDATE Clasificacion SET t1='"+seg3a+"',t2='"+seg3b+"' where segmento=3;")
        cursorObj.execute("UPDATE Clasificacion SET t1='"+seg4a+"',t2='"+seg4b+"' where segmento=4;")
        self.con.commit()
    # Función de comprobar usuario autentificado
    # Se le pasarán los datos del label y hará una consulta a la base de datos
    # Comprobando si los datos introducidos coinciden con los de la base de datos
    # Si coinciden devolvera un 1 si existe y coincide.
    def sql_ComprobarUsuario(self,usuario,contraseña):
        res = False
        cursorObj = self.con.cursor()
        contraseña = str.encode(contraseña)
        h = hashlib.sha1(contraseña)
        contraseña=h.hexdigest()
        cursorObj.execute("SELECT count(usuario) FROM Usuarios where usuario='"+usuario+"' and password='"+contraseña+"'")
        num = cursorObj.fetchone()[0]
        print(type(num))
        if num>0:
            res= True
        else:
            res= False
        return res
    # Función para comprobar la existencia de las tablas
    # Hace la petición a la base de datos con el nombre de las tablas
    # Nos servirá para poder comprobar si existen devolvendo un true o un false
    def sql_ComprobarTabla(self):
        existencia = False
        cursorObj = self.con.cursor()

        cursorObj.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Usuarios' ''')
        if cursorObj.fetchone()[0]==1 :
            existencia= True
        else:
            existencia= False
        return existencia
    # Función para conseguir los nombres de los pacientes en la base de datos
    # Hará una peticion a la base de datos para que nos devuelva sus nombres
    # Y nos devolverá una lista de los pacientes
    def sql_getPacientes(self):
        
        cursorObj=self.con.cursor()
        cursorObj.execute(''' SELECT nombre FROM Pacientes ''')
        results=cursorObj.fetchall()
        Pacientes=[]

        item_0_in_result = [_[0] for _ in results]

        for paciente in item_0_in_result:
            Pacientes.append(paciente)
        return Pacientes
    #
    #Función que nos dará las los tiempos de cada segmento y el total que se usará
    #Para identificar la gravedad del paciente
    #
    def sql_getClasificacion(self):
        cursorObj=self.con.cursor()
        cursorObj.execute(''' SELECT t1,t2 FROM Clasificacion ''')
        results = cursorObj.fetchall()
        Clasi=[]
        Clasi.append([_[0] for _ in results])
        Clasi.append([_[1] for _ in results])
        return Clasi

    # Función para conseguir todos los datos de un paciente
    # Hara una petición para que nos devuelvan todos los datos
    # Devolverá una lista con los datos del paciente consultado
    def sql_getDatosPacientes(self,nombre):
        cursorObj=self.con.cursor()
        cursorObj.execute(" SELECT nombre,apellido,SIP,nacimiento,gravedad,medicacion FROM Pacientes where nombre='"+nombre+"'" )
        results=cursorObj.fetchall()
        Pacientes=[]

        Pacientes.append([_[0] for _ in results])
        Pacientes.append([_[1] for _ in results])
        Pacientes.append([_[2] for _ in results])
        Pacientes.append([_[3] for _ in results])
        Pacientes.append([_[4] for _ in results])
        Pacientes.append([_[5] for _ in results])
        
        return Pacientes
    # Función para mostrar los tiempos
    # Hará una petición que nos devolverá los tiempos
    # E irá añadiendolos a una lista y le daremos los datos a la gráfica
    # La cual se la pasamos a la función y una vez tiene los datos
    # Los dibujamos
    def sql_MostrarGrafica(self,grafica,nombre):
        global comprobado
        cursorObj=self.con.cursor()
        cursorObj.execute("SELECT count(*) FROM Pruebas WHERE paciente='"+nombre+"'")
        if cursorObj.fetchone()[0]>=1 :
            cursorObj.execute("SELECT fecha,TiempoTotal,lap1,lap2,lap3 FROM Pruebas where paciente='"+nombre+"'")
            data=cursorObj.fetchall()
            dates = []
            values = []
            lap1 = []
            lap2 = []
            lap3 = []
            for row in data:
                dates.append((row[0]))
                values.append((row[1]))
                lap1.append((row[2]))
                lap2.append((row[3]))
                lap3.append((row[4]))
            grafica.clear()
            datesdict = dict(enumerate(dates))
            grafica.addLegend()
            grafica.showGrid(x=True,y=True)
            grafica.plot(list(datesdict.keys()),values,name="Tiempo total",symbol="+",symbolSize=10,symbolBrush=("r"))
            grafica.plot(list(datesdict.keys()),lap1,name="Segmento 1",symbol="+",symbolSize=10,symbolBrush=("b"))
            grafica.plot(list(datesdict.keys()),lap2,name="Segmento 2",symbol="+",symbolSize=10,symbolBrush=("b"))
            grafica.plot(list(datesdict.keys()),lap3,name="Segmento 3",symbol="+",symbolSize=10,symbolBrush=("b"))
            global lienzo 
            comprobado = 1
        else:
            comprobado = 0
    # Función para guardar los tiempos de la prueba
    # Se le pasará el nombre y el tiempo que ha tardado en realizar la prueba
    # Hará un insert a la base de datos con los datos y la fecha en la que se ha realizado el guardado
    def sql_GuardarPrueba(self,paciente,segmento1,segmento2,segmento3,total):
        cursorObj = self.con.cursor()
        cursorObj.execute("INSERT INTO Pruebas(paciente,lap1,lap2,lap3,TiempoTotal,fecha) VALUES('"+paciente+"',"+segmento1+","+segmento2+","+segmento3+","+total+",datetime('now','localtime'))")
        print("Hola")
        self.con.commit()
    #
    #Función que usaremos para añadir un usuario válido que pueda acceder al programa
    #
    def sql_InsertarUsuario(self,nombre,contraseña):
        cursorObj = self.con.cursor()
        ccifrada = Cifrar.Cifrar().CifrarTexto(contraseña)
        cursorObj.execute('INSERT INTO Usuarios(usuario,password) VALUES("'+nombre+'","'+ccifrada+'");')
        self.con.commit()
    #
    #Función que comprobará si existe algún usuario además del root
    #Para que la primera vez que se inicie el programa nos permita añadir un usuario
    #
    def sql_ComprobarUsuarioDoctor(self):
        existencia = False
        cursorObj = self.con.cursor()
        cursorObj.execute(''' SELECT count(usuario) FROM Usuarios ''')
        if cursorObj.fetchone()[0]==1 :
            existencia= True
        else:
            existencia= False
        return existencia
    #
    #Función que nos devolverá la información del paciente que será mostrada cuando usemos el botón
    #De más información
    #
    def sql_getExtra(self,nombre):
        cursorObj=self.con.cursor()
        cursorObj.execute(" SELECT direccion,email,telefono,genero,fechaingreso,IMC,grasacorporal,altura,peso,DNI FROM Pacientes where nombre='"+nombre+"'" )
        results=cursorObj.fetchall()
        Pacientes=[]

        Pacientes.append([_[0] for _ in results])
        Pacientes.append([_[1] for _ in results])
        Pacientes.append([_[2] for _ in results])
        Pacientes.append([_[3] for _ in results])
        Pacientes.append([_[4] for _ in results])
        Pacientes.append([_[5] for _ in results])
        Pacientes.append([_[6] for _ in results])
        Pacientes.append([_[7] for _ in results])
        Pacientes.append([_[8] for _ in results])
        Pacientes.append([_[9] for _ in results])
        
        return Pacientes
    #
    #Función que actualizará la nueva información modificada del apartado de más información
    #
    def sql_ActualizarExtraPaciente(self,nombre,dni,direccion,correo,telefono,genero,IMC,grasacorporal,altura,peso):
        cursorObj = self.con.cursor()
        cursorObj.execute("UPDATE Pacientes SET DNI='"+dni+"',direccion='"+direccion+"',email='"+correo+"',Telefono='"+telefono+"',genero='"+genero+"',IMC='"+IMC+"',grasacorporal='"+grasacorporal+"',altura='"+peso+"',peso='"+peso+"' where nombre='"+nombre+"';")
        self.con.commit()