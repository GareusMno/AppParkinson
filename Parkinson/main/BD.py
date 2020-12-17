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

#Conexion con la base de datos
#
#Coenctamos con la base de datos y si ya existe, se conectará

class Base(object):
    def __init__(self):
        self.con=""
        try:
            
            self.con = sqlite3.connect(Path.joinpath(Path(__file__).parent.parent,"bd/Parkinson.db"))

        except Error:

            print(Error)

    def sql_CreateTable(self):
        cursorObj = self.con.cursor()

        cursorObj.execute("CREATE TABLE Usuarios(usuario String PRIMARY KEY not null default root, password String not null default root);")
        cursorObj.execute('INSERT INTO Usuarios(usuario, password) VALUES("root", "dc76e9f0c0006e8f919e0c515c66dbba3982f785");')
        cursorObj.execute("CREATE TABLE Pacientes(codigo INTEGER PRIMARY KEY AUTOINCREMENT, paciente String not null, gravedad INTEGER ,edad INTEGER);")
        cursorObj.execute('INSERT INTO Pacientes(paciente,gravedad,edad) VALUES("Pepe Garcia",1,25);')
        cursorObj.execute("CREATE TABLE Pruebas(codigo INTEGER PRIMARY KEY AUTOINCREMENT, paciente String not null, tiempo INTEGER ,fecha String);")
        cursorObj.execute('INSERT INTO Pruebas(paciente,tiempo,fecha) VALUES("Pepe Garcia",67,"  23/1/2000");')
        cursorObj.execute('INSERT INTO Pruebas(paciente,tiempo,fecha) VALUES("Pepe Garcia",43,"  23/2/2000");')
        self.con.commit()
    def sql_InsertarPaciente(self,paciente,gravedad):
        cursorObj = self.con.cursor()
        cursorObj.execute('INSERT INTO Pacientes(paciente,gravedad) VALUES("'+paciente+'",'+gravedad+');')
        con.commit()
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
    def sql_ComprobarTabla(self,nombre):
        existencia = False
        cursorObj = self.con.cursor()

        cursorObj.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Usuarios' ''')
        if cursorObj.fetchone()[0]==1 :
            existencia= True
        else:
            existencia= False
        return existencia

    def sql_getPacientes(self):
        
        cursorObj=self.con.cursor()
        cursorObj.execute(''' SELECT paciente FROM Pacientes ''')
        results=cursorObj.fetchall()
        Pacientes=[]

        item_0_in_result = [_[0] for _ in results]

        for paciente in item_0_in_result:
            Pacientes.append(paciente)
        return Pacientes

    def sql_getDatosPacientes(self,nombre):
        cursorObj=self.con.cursor()
        cursorObj.execute(" SELECT paciente,gravedad,edad FROM Pacientes where paciente='"+nombre+"'" )
        results=cursorObj.fetchall()
        Pacientes=[]

        Pacientes.append([_[0] for _ in results])
        Pacientes.append([_[1] for _ in results])
        Pacientes.append([_[2] for _ in results])

        
        return Pacientes

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