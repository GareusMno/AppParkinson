import hashlib
prueba="asdasd"
texto = str.encode(prueba)
h = hashlib.sha1(texto)
print (h.hexdigest())
contra="dc76e9f0c0006e8f919e0c515c66dbba3982f785"
if (h.hexdigest()==contra):
    print("Coinciden")
