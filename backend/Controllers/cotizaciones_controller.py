from flask import jsonify, request
from Services.cotizaciones_services import servListCotizaciones, servAddCotizaciones, servDelCotizaciones, servModCotizaciones

def cntListCotizaciones():
    data = servListCotizaciones()
    return jsonify(data), 200

def cntAddCotizaciones():
    data = servAddCotizaciones()
    return jsonify(data), 200

def cntDelCotizaciones():
    data = servDelCotizaciones()
    return jsonify(data), 200

def cntModCotizaciones():
    data = servModCotizaciones()
    return jsonify(data), 201

