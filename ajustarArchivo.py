def ajustarArchivo(archivo):
    file = open(archivo, "r")
    texto = file.readline().strip()
    file.close()
    lineas = texto.split("empty")
    lineas.pop()
    file = open(archivo, "w")
    for l in lineas:
        file.write(l + "empty\n")
    file.close()

ajustarArchivo("test.txt")