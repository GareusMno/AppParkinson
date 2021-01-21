import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
ruta = os.path.normpath(os.path.join(os.getcwd(),".."))
ruta2 = os.path.normpath(os.path.join(ruta,".."))
sys.path.append(os.path.normpath(os.path.join(ruta,"..")))
from main import ParkinsonV2

if __name__ == "__main__":
    #Instalará los programas necesarios para la ejecución del programa
    os.system("pip3 install -r ."+os.path.sep+"requirements.txt")
    app = QApplication(sys.argv)
    ex = ParkinsonV2.MainWindow()
    sys.exit(app.exec_())
    
