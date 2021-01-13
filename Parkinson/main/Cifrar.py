import hashlib

class Cifrar():
    def __init__(self):
        self.prueba=""
    def CifrarTexto(self,texto):
        codificado = str.encode(texto)
        h = hashlib.sha1(codificado)
        codificado=h.hexdigest()
        return codificado