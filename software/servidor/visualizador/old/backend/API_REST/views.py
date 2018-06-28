"""
Routes and views for the flask application.
"""


from datetime import datetime
from flask import render_template, request, jsonify, json
import pymongo
from API_REST import app
from http import HTTPStatus
from random import randint,choice
# encoding=utf8
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

mongo = pymongo.MongoClient(host='localhost',port=27017)

mongo_config = mongo.redes.config
mongo_datos = mongo.redes.datos
#mongo.redes.datos.create_index([( "geometry",pymongo.GEOSPHERE)])


@app.route('/ultimo', methods = ['GET'])
def get_last():
    """Muestra los ultimos datos de una habitacion dada"""
    result = []
    habitacion = request.args.get('habitacion',type=str)
    datos = mongo_datos.find_one().sort("_id", -1)
    if datos.count() > 0:
        header = HTTPStatus.OK
        for dato in datos:
            result.append(dato)
    else:
        header = HTTPStatus.NOT_FOUND
    return json.dumps(result), header


@app.route('/add', methods = ['POST'])
def add_data():
    """Anade datos recogidos de una habitacion"""
    data = request.get_json()
    if not data:
        header = HTTPStatus.BAD_REQUEST
        body = "Datos vacios"
    else:
        habitacion = data.get('habitacion')
        if habitacion:
            mongo_datos.insert(data)
            header = HTTPStatus.CREATED
            body = habitacion
        else:
            header = HTTPStatus.BAD_REQUEST
            body = "La habitacion es obligatoria"

    return json.dumps({'body': body}), header

@app.route('/grafico', methods = ['GET'])
def get_grafico():
    return render_template('index.html')

@app.route('/historico', methods = ['GET'])
def get_historico():
    return jsonify({
		"raceDate": "06/25/2017 10:00:00",
		"raceName": choice(["Carrera Velocidad","Carrera Resistencia","Carrera Maniobrabilidad"]),
		#"status": choice(["abort","design","briefing","waiting","launch","start"]),
		"status":"start",
		"windDirection":randint(0,360),
		"windIntensity": randint(0,10),			
        "time": '0',
		"startLine":[[42.124508, -8.846614],[42.124829, -8.846494]],
		"finishLine":[[42.124590, -8.845174],[42.124192, -8.845346]],
        'boyas':[{
			'nombre':'boya1',
			'tipo':'real',
            'localizacion': [42.124508, -8.846614]
        },
		{
			'nombre':'boya2',
			'tipo':'real',
            'localizacion': [42.124829, -8.846494]
        },{
			'nombre':'boya3',
			'tipo':'virtual',
            'localizacion': [42.124 + randint(5,8)/10000, -8.846 - randint(1,2)/10000]
        }],
        'barcos': [{
            'nombre':'Hogar1',
			'tipo': 'monocasco',
            'velocidad': randint(0, 9),
            'power': randint(20,40),
            'posicion': randint(1,13),
            'temperatura': randint(0, 40),
            'color': '#1f78b4',
			'nombreColor':'azul_oscuro',
            'localizacion': [42.124 + randint(1,9)/10000, -8.846 - randint(1,9)/10000],
            'direccion' : randint(1, 359)
        },{
            'nombre':'Montecastelo',
			'tipo':'bicasco',
            'velocidad': randint(0, 9),
            'power': randint(20,40),
            'posicion': randint(1,13),
            'temperatura': randint(0, 40),
            'color': '#b2df8a',
			'nombreColor':'verde_claro',
            'localizacion': [42.124 + randint(1,9)/10000, -8.846 - randint(1,9)/10000],
            'direccion' : randint(1, 359)
        },
		{
            'nombre':'Barco3',
			'tipo':'bicasco',
            'velocidad': randint(0, 9),
            'power': randint(20,40),
            'posicion': randint(1,13),
            'temperatura': randint(0, 40),
            'color': '#cab2d6',
			'nombreColor':'violeta',
            'localizacion': [42.124 + randint(1,9)/10000, -8.846 - randint(1,9)/10000],
            'direccion' : randint(1, 359)
        },
		{
            'nombre':'Iluminados del Caribe',
			'tipo':'bicasco',
            'velocidad': randint(0, 9),
            'power': randint(20,40),
            'posicion': randint(1,13),
            'temperatura': randint(0, 40),
            'color': '#e78ac3',
			'nombreColor':'rosa',
            'localizacion': [42.124 + randint(1,9)/10000, -8.846 - randint(1,9)/10000],
            'direccion' : randint(1, 359)
        },
		{
            'nombre':'Castelao',
			'tipo':'tricasco',
            'velocidad': randint(0, 9),
            'power': randint(20,40),
            'posicion': randint(1,13),
            'temperatura': randint(0, 40),
            'color': '#fdbf6f',
			'nombreColor':'naranja_claro',
            'localizacion': [42.124 + randint(1,9)/10000, -8.846 - randint(1,9)/10000],
            'direccion' : randint(1, 359)
        }]
    })

'''
@app.route('/barco/<matricula>' , methods=['PUT'])
def put_barco(matricula):
    """Actualiza el barco con los datos recibidos"""
    data = request.get_json()

    if not data:
        header = HTTPStatus.BAD_REQUEST
        body = "Datos vacios"
    else:
        if "hora" in data["properties"]:
            data["properties"]["hora"] = dateutil.parser.parse(data["properties"]["hora"])
        if matricula:
            if mongo.redes.barcos.find_one({"matricula": matricula}):
                mongo.redes.barcos.update_one({'matricula': matricula},{"$set": data}, upsert=False)
                header = HTTPStatus.OK
                body = "";
            else:
                header = HTTPStatus.NOT_FOUND
                body = "Barco no dado de alta en el sistema"
        else:
            header = HTTPStatus.BAD_REQUEST
            body = "Matricula es obligatoria"

    return json.dumps({'body': body}), header
'''

