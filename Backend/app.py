from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from xml.dom import minidom
import re
from analizador import *
from time import *


app = Flask(__name__)
CORS(app)

@app.route('/CargarArchivo', methods=['POST'])
def CargarArchivo():
    data = request.json
    ruta = data['Ruta']
    archivo = minidom.parse(ruta)
    a = obtenerMensajes(archivo)
    b = obtenerSentimientosPositivos(archivo)
    c = obtenerSentimientosNegativos(archivo)
    d = obtenerEmpresas(archivo)
    e = obtenerServicios(archivo)
    baseDeDatos(a,b,c,d,e)
    return 'Archivo Cargado'

@app.route('/reset', methods=['GET'])
def Reset():
    reset()
    return 'Datos Borrados'

@app.route('/ConsultarDatos', methods=['GET'])
def consultarDatos():
    y = []
    archivo = minidom.parse('DataBase.xml')
    mensajes = obtenerMensajes(archivo)
    print(mensajes)
    for mensaje in mensajes:
        x = response1(mensaje)
        y.append(x)
        reporte(y)
    return jsonify(y)

@app.route('/ProcesarMensaje', methods=['POST'])
def ProcesarMensaje():
    data = request.json
    mensaje = data['Mensaje']
    x = response1(mensaje)
    reporte(x)
    return jsonify(x)

@app.route('/ConsultarFecha', methods=['POST'])
def consultarFecha():
    y = []
    z = []
    data = request.json
    archivo = minidom.parse('DataBase.xml')
    x = obtenerMensajes(archivo)
    empresa = data['Empresa']
    m = ['Fecha:',data['Fecha']]
    y.append(m)
    if empresa !=  'All':
        for i in x:
            if data['Fecha'] == FobtenerFecha(i) and empresaMensaje(i,data['Empresa']):
                n = response1(i)
                y.append(n)
        reporte(y)
        return jsonify(y)
    else:
        y = obtenerEmpresas(archivo)
        for i in x:
            for j in y:
                if data['Fecha'] == FobtenerFecha(i) and empresaMensaje(i,j):
                    n = response1(i)
                    z.append(n)
        reporte(z)
        return jsonify(z)

@app.route('/ConsultarRangoFechas', methods=['POST'])
def consultarRangoFechas():
    y = []
    z = []
    data = request.json
    archivo = minidom.parse('DataBase.xml')
    x = obtenerMensajes(archivo)
    empresa = data['Empresa']
    mI = ['FechaInicial:', data['FechaInicial']]
    mF = ['FechaFinal:', data['FechaFinal']]
    z.append(mI)
    z.append(mF)
    inicio = data['FechaInicial']
    fin = data['FechaFinal']
    lista_fechas = [(datetime.strptime(inicio,"%d/%m/%Y") + timedelta(days=d)).strftime("%d/%m/%Y")
                    for d in range((datetime.strptime(fin,"%d/%m/%Y") - datetime.strptime(inicio,"%d/%m/%Y")).days + 1)] 
    for fecha in lista_fechas:
        if empresa !=  'All':
            for i in x:
                if fecha == FobtenerFecha(i) and empresaMensaje(i,data['Empresa']):
                    n = response1(i)
                    z.append(n)
        else:
            y = obtenerEmpresas(archivo)
            for i in x:
                for j in y:
                    if fecha == FobtenerFecha(i) and empresaMensaje(i,j):
                        n = response1(i)
                        z.append(n)
    reporte(z)
    return jsonify(z)


if __name__ == '__main__':
    app.run(port=5000)

