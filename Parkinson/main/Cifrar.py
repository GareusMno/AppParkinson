import hashlib
#
#Cifra la el texto que le pases y te lo devuelve codificado
#
class Cifrar():
    def __init__(self):
        self.prueba=""
    def CifrarTexto(self,texto):
        codificado = str.encode(texto)
        h = hashlib.sha1(codificado)
        codificado=h.hexdigest()
        return codificado