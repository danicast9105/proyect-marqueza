from flask import jsonify, request
from Services.ventas_services import servListVentas, servAddVentas, servDelVentas, servModVentas

def cntListVentas():
    data = servListVentas()
    return jsonify(data), 200

def cntAddVentas():
    data = servAddVentas()
    return jsonify(data), 200

def cntDelVentas():
    data = servDelVentas()
    return jsonify(data), 200

def cntModVentas():
    data = servModVentas()
    return jsonify(data), 201

