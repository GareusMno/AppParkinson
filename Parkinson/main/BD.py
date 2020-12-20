import sqlite3
import hashlib
import os

from sqlite3 import Error
from pathlib import Path
from dateutil import parser

import matplotlib.pyplot as plt
import datetime
import numpy as np
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# Clase de la base de datos que al crearla y anos ofrecerá la conexion
# Con la base de datos y nos permitira acceder a todas las funciones
# Relacionadas con la base de datos
class Base(object):
    def __init__(self):
        self.con=""
        try:
            
            self.con = sqlite3.connect(Path.joinpath(Path(__file__).parent.parent,"bd/Parkinson.db"))

        except Error:

            print(Error)
    # Función de crear tablas
    # Función que se ejecutará al principio y creará las tablas vacías
    # De la base de datos para que podamos trabajar con ellas
    def sql_CreateTable(self):
        cursorObj = self.con.cursor()

        cursorObj.execute("CREATE TABLE Usuarios(usuario String PRIMARY KEY not null default root, password String not null default root);")
        cursorObj.execute('INSERT INTO Usuarios(usuario, password) VALUES("root", "dc76e9f0c0006e8f919e0c515c66dbba3982f785");')
        cursorObj.execute("CREATE TABLE Pacientes(codigo INTEGER PRIMARY KEY AUTOINCREMENT, paciente String not null, gravedad INTEGER ,edad INTEGER);")
        cursorObj.execute('INSERT INTO Pacientes(paciente,gravedad,edad) VALUES("Pepe Garcia",1,25);')
        cursorObj.execute("CREATE TABLE Pruebas(codigo DECIMAL PRIMARY KEY AUTOINCREMENT, paciente String not null, tiempo INTEGER ,fecha String);")
        cursorObj.execute('INSERT INTO Pruebas(paciente,tiempo,fecha) VALUES("Pepe Garcia",67,"  23/1/2000");')
        cursorObj.execute('INSERT INTO Pruebas(paciente,tiempo,fecha) VALUES("Pepe Garcia",43,"  23/2/2000");')
        self.con.commit()
    # Función de insertar pacientes
    # Se ejecutará cuando queramos añadir nuevos pacientes
    # Nos pasarán los datos de cada paciente por parámetros y le haremos un insert a la base de datos
    def sql_InsertarPaciente(self,paciente,gravedad):
        cursorObj = self.con.cursor()
        cursorObj.execute('INSERT INTO Pacientes(paciente,gravedad) VALUES("'+paciente+'",'+gravedad+');')
        self.con.commit()
    # Función de actualizar pacientes
    # Se ejecutará cuando modifiquemos un paciente
    # Que hara un update según los datos actualizados que le serán pasados por parámetros
    def sql_ActualizarPaciente(self,paciente,gravedad,edad):
        cursorObj = self.con.cursor()
        cursorObj.execute('UPDATE Pacientes SET (paciente="'+paciente+'",gravedad='+gravedad+'",edad='+edad+');')
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
    def sql_ComprobarTabla(self,nombre):
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
        cursorObj.execute(''' SELECT paciente FROM Pacientes ''')
        results=cursorObj.fetchall()
        Pacientes=[]

        item_0_in_result = [_[0] for _ in results]

        for paciente in item_0_in_result:
            Pacientes.append(paciente)
        return Pacientes
    # Función para conseguir todos los datos de un paciente
    # Hara una petición para que nos devuelvan todos los datos
    # Devolverá una lista con los datos del paciente consultado
    def sql_getDatosPacientes(self,nombre):
        cursorObj=self.con.cursor()
        cursorObj.execute(" SELECT paciente,gravedad,edad FROM Pacientes where paciente='"+nombre+"'" )
        results=cursorObj.fetchall()
        Pacientes=[]

        Pacientes.append([_[0] for _ in results])
        Pacientes.append([_[1] for _ in results])
        Pacientes.append([_[2] for _ in results])

        
        return Pacientes
    # Función para mostrar los tiempos
    # Hará una petición que nos devolverá los tiempos
    # E irá añadiendolos a una lista y le daremos los datos a la gráfica
    # La cual se la pasamos a la función y una vez tiene los datos
    # Los dibujamos
    def sql_MostrarGrafica(self,grafica):
        cursorObj=self.con.cursor()
        cursorObj.execute("SELECT fecha,tiempo FROM Pruebas")
        data=cursorObj.fetchall()
        dates = []
        values = []
        for row in data:
            dates.append(row[0])
            values.append((row[1]))
        grafica.axes.plot(dates, values,"r")
        grafica.draw()
    # Función para guardar los tiempos de la prueba
    # Se le pasará el nombre y el tiempo que ha tardado en realizar la prueba
    # Hará un insert a la base de datos con los datos y la fecha en la que se ha realizado el guardado
    def sql_GuardarPrueba(self,paciente,tiempo):
        cursorObj = self.con.cursor()
        cursorObj.execute("INSERT INTO Pruebas(paciente,tiempo,fecha) VALUES('"+paciente+"',"+tiempo+",datetime('now','localtime'))")
        self.con.commit()
