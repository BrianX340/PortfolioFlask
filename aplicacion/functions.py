import hashlib




def encriptar_password(clave):
    passw = hashlib.new("sha1", clave.encode("utf-8"))
    return passw.hexdigest()

