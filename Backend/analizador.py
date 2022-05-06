from xml.dom import minidom
from xml.etree import ElementTree as ET
import webbrowser
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
        palabras = elem.getElementsByTagName('servicio')
        for palabra in palabras:
            n = palabra.getElementsByTagName('alias')
            x = []
            for i in n:
                y = i.firstChild.data
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

###########################################################################
###########################################################################

def FobtenerFecha(mensaje):
    x = re.findall('[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]', mensaje, flags=re.IGNORECASE)
    if x != []:
        return x[0]

def FcantidadMensajesTotal(mensajes:list, empresa:str):
    
    if empresa == 0:
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

def empresaMensaje(mensaje:str, empresa:str):
    x = re.findall(empresa, mensaje,flags=re.IGNORECASE)
    if len(x) != 0:
        return True
    else:
        return False

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

def baseDeDatos(mensajes: list, sentimientosPositivos: list, sentimientosNegativos:list,empresas:list, servicios:list):
    f = open('DataBase.xml','r+')
    if f.read() != '':
        archivo = minidom.parse('DataBase.xml')
        a = obtenerMensajes(archivo)
        b = obtenerSentimientosPositivos(archivo)
        c = obtenerSentimientosNegativos(archivo)
        d = obtenerEmpresas(archivo)
        e = obtenerServicios(archivo)
        for i in a:
            mensajes.append(i)
        for i in b:
            sentimientosPositivos.append(i)
        for i in c:
            sentimientosNegativos.append(i)
        for i in d:
            empresas.append(i)
        for i in e:
            servicios.append(i)

    archivo = ET.Element('solicitud_clasificacion')
    diccrionario = ET.SubElement(archivo,'diccionario')
    positif = ET.SubElement(diccrionario,'sentimientos_positivos')
    
    for i in sentimientosPositivos:
        palabras = ET.SubElement(positif,'palabra')
        palabras.text=i

    negatif = ET.SubElement(diccrionario,'sentimientos_negativos')
    
    for i in sentimientosNegativos:
        palabras = ET.SubElement(negatif,'palabra')
        palabras.text=i
    
    empresasA = ET.SubElement(diccrionario, 'empresas_analizar')
    empresa = ET.SubElement(empresasA, 'empresa')
    for i in empresas:
        nombre = ET.SubElement(empresa,'nombre')
        nombre.text = i
        contador = 0
        for j in servicios[0]:
            servicio = ET.SubElement(empresa,'servicio')
            servicio.set('nombre', j)
            for i in servicios[contador+1]:
                alias = ET.SubElement(servicio,'alias')
                alias.text = i
            contador += 1
    lista = ET.SubElement(archivo,'lista_mensajes')
    for i in mensajes:
        men = ET.SubElement(lista, 'mensaje')
        men.text = i

    f = open('DataBase.xml','w')
    mydata1 = str(ET.tostring(archivo))
    mydata2 = re.sub('b\'','',mydata1)
    mydata = re.sub('\'','',mydata2)
    f.write(str(mydata))

def response1(mensaje):
    archivo = minidom.parse('DataBase.xml')
    b = obtenerSentimientosPositivos(archivo)
    c = obtenerSentimientosNegativos(archivo)
    d = obtenerEmpresas(archivo)
    e = obtenerServicios(archivo)
    x = clasifMensajeSent(mensaje,b,c)
    for i in range(0,len(d)):
        for j in range(0,len(e[0])):
            y = clasifMensajeServ(mensaje, d[i], e[0][j])
            if y == True:
                return x,d[i], e[0][j]
        for j in range(1,len(e)):
            for k in range(0,len(e[j])):
                y = clasifMensajeServ(mensaje, d[i], e[j][k])
                if y == True:
                    return x,d[i], e[0][j-1]

def reset():
    f = open('DataBase.xml','w')
    f.write('')

def reporte(data):
    f = open('reporte.html','w')
    f.write(str(data))
    webbrowser.open('reporte.html')

