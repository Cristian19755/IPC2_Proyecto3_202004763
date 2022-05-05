from xml.dom import minidom
import re

def obtenerSentimientosPositivos(archivo):
    x = []
    archivo = archivo.getElementsByTagName('sentimientos_positivos')
    for elem in archivo:
        palabras = elem.getElementsByTagName('palabra')
        for palabra in palabras:
            y = palabra.firstChild.data
            y = y.replace(' ', '')
            y = simplificar(y)
            contador = 0
            if len(x) == 0:
                x.append(y)
            else:
                for i in range(0,len(x)):
                    z = re.findall(y,x[i],flags=re.IGNORECASE)
                    if z == []:
                        contador += 1
                if contador == len(x):
                    x.append(y)
                    contador = 0
    return x

def simplificar(s):
    remplazos = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("\n", "")
    )
    for a, b in remplazos:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def obtenerSentimientosNegativos(archivo):
    x = []
    archivo = archivo.getElementsByTagName('sentimientos_negativos')
    for elem in archivo:
        palabras = elem.getElementsByTagName('palabra')
        for palabra in palabras:
            y = palabra.firstChild.data
            y = y.replace(' ', '')
            y = simplificar(y)
            contador = 0
            if len(x) == 0:
                x.append(y)
            else:
                for i in range(0,len(x)):
                    z = re.findall(y,x[i],flags=re.IGNORECASE)
                    if z == []:
                        contador += 1
                if contador == len(x):
                    x.append(y)
                    contador = 0
    return x

def obtenerEmpresas(archivo):
    x = []
    archivo = archivo.getElementsByTagName('empresa')
    for elem in archivo:
        palabras = elem.getElementsByTagName('nombre')
        for palabra in palabras:
            y = palabra.firstChild.data
            y = y.replace(' ', '')
            y = simplificar(y)
            contador = 0
            if len(x) == 0:
                x.append(y)
            else:
                for i in range(0,len(x)):
                    z = re.findall(y,x[i],flags=re.IGNORECASE)
                    if z == []:
                        contador += 1
                if contador == len(x):
                    x.append(y)
                    contador = 0
    return x

def obtenerServicios(archivo):
    x = []
    serv = []
    servicios = []
    archivo = archivo.getElementsByTagName('empresa')
    for elem in archivo:
        serv = []
        j = elem.getElementsByTagName('servicio')
        for i in j:
            y = i.attributes['nombre'].value
            y = y.replace(' ', '')
            y = simplificar(y)
            contador = 0
            if len(serv) == 0:
                serv.append(y)
            else:
                for i in range(0,len(serv)):
                    z = re.findall(y,serv[i],flags=re.IGNORECASE)
                    if z == []:
                        contador += 1
                if contador == len(serv):
                    serv.append(y)
                    contador = 0
    servicios.append(serv)

    for elem in archivo:
        x = []
        palabras = elem.getElementsByTagName('alias')
        for palabra in palabras:
            y = palabra.firstChild.data
            y = y.replace(' ', '')
            y = simplificar(y)
            contador = 0
            if len(x) == 0:
                x.append(y)
            else:
                for i in range(0,len(x)):
                    z = re.findall(y,x[i],flags=re.IGNORECASE)
                    if z == []:
                        contador += 1
                if contador == len(x):
                    x.append(y)
                    contador = 0
        servicios.append(x)
    return servicios

def obtenerMensajes(archivo):
    x = []
    archivo = archivo.getElementsByTagName('lista_mensajes')
    for elem in archivo:
        palabras = elem.getElementsByTagName('mensaje')
        for palabra in palabras:
            y = palabra.firstChild.data
            y = simplificar(y)
            contador = 0
            if len(x) == 0:
                x.append(y)
            else:
                for i in range(0,len(x)):
                    z = re.findall(y,x[i],flags=re.IGNORECASE)
                    if z == []:
                        contador += 1
                if contador == len(x):
                    x.append(y)
                    contador = 0
    return x

def obtenerMensajeInd(archivo):
    x = []
    palabras = archivo.getElementsByTagName('mensaje')
    for palabra in palabras:
        y = palabra.firstChild.data
        y = simplificar(y)
        contador = 0
        if len(x) == 0:
            x.append(y)
        else:
            for i in range(0,len(x)):
                z = re.findall(y,x[i],flags=re.IGNORECASE)
                if z == []:
                    contador += 1
            if contador == len(x):
                x.append(y)
                contador = 0
    return x
###########################################################################
###########################################################################

def FobtenerFecha(mensaje):
    x = re.findall('[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]', mensaje, flags=re.IGNORECASE)
    return x[0]

def FcantidadMensajesTotal(mensajes:list):
    num = len(mensajes)
    return num

def clasifMensajeSent(mensaje:str, positivos:list, negativos:list):
    pos = 0
    neg = 0
    for i in positivos:
        x = re.findall(i,mensaje,flags=re.IGNORECASE)
        pos += len(x)
    for i in negativos:
        x = re.findall(i,mensaje,flags=re.IGNORECASE)
        neg += len(x)
    total = pos - neg
    if total == 0:
        return 'neutro'
    elif total < 0:
        return 'negativo'
    elif total > 0:
        return 'positivo'

def numMenServ(mensajes:list, empresa: str):
    num = 0
    for i in mensajes:
        x = re.findall(empresa,i,flags=re.IGNORECASE)
        if len(x) != 0:
            num += 1
    return num

def clasifMensajeServ(mensaje:str, empresa:str, servicio:str):
    x = re.findall(empresa,mensaje,flags=re.IGNORECASE)
    y = re.findall(servicio, mensaje, flags=re.IGNORECASE)
    if len(x) != 0 and len(y) != 0:
        return True
    else:
        return False

def salida():
    x = ''''''

'''
archive = minidom.parse('db.xml')
y = obtenerSentimientosPositivos(archive)
z = obtenerSentimientosNegativos(archive)
x = obtenerMensajes(archive)

for i in x:
    print(clasifMensajeSent(i,y,z))
print(numMenServ(x,'USAC'))'''