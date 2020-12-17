import os
import sys
import sqlite3
print(os.path.dirname(sys.path[0]),"prueba")

from pathlib import Path


con = sqlite3.connect(Path.joinpath(Path(__file__).parent.parent.parent,"bd/Parkinson.db"))
cursorObj=con.cursor()
cursorObj.execute(" SELECT paciente,edad,gravedad FROM Pacientes where paciente='Pepe Garcia'" )
results=cursorObj.fetchall()
datos=[]

nombre = [_[0] for _ in results] 
edad = [_[1] for _ in results]
gravedad = [_[2] for _ in results]

datos.append(nombre)
datos.append(edad)
datos.append(gravedad)
