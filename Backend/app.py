from flask import Flask, jsonify, request
from flask_cors import CORS
from xml.dom import minidom
import re
from analizador import *


app = Flask(__name__)
CORS(app)

@app.route('/ProcesarMensaje', methods=['POST'])
def ProcesarMensaje():
    data = request.json
    mensaje = data['Mensaje']
    x = response1(mensaje)
    return jsonify(x)

@app.route('/ConsultarFecha', methods=['POST'])
def consultarFecha():
    y = []
    z = []
    data = request.json
    ruta = data['Ruta']
    archivo = minidom.parse(ruta)
    x = obtenerMensajes(archivo)
    empresa = data['Empresa']
    if empresa !=  'All':
        for i in x:
            if data['Fecha'] == FobtenerFecha(i) and empresaMensaje(i,data['Empresa']):
                y.append(i)
        return jsonify(y)
    else:
        y = obtenerEmpresas(archivo)
        for i in x:
            for j in y:
                if data['Fecha'] == FobtenerFecha(i) and empresaMensaje(i,j):
                    z.append(i)
        return jsonify(z)


if __name__ == '__main__':
    app.run(port=5000)

