from flask import jsonify, request
from Services.cotizaciones_services import servListCotizaciones, addCotizaciones, deleteCotizaciones, updateCotizaciones

def cntListCotizaciones():
    data = servListCotizaciones()
    return jsonify(data), 200

def cntAddCotizaciones():
    data = addCotizaciones()
    return jsonify(data), 200

def cntDelCotizaciones():
    data = deleteCotizaciones()
    return jsonify(data), 200

def cntModCotizaciones():
    data = updateCotizaciones()
    return jsonify(data), 201

