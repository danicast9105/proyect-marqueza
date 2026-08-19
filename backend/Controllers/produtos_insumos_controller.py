from flask import jsonify, request
from Services.produtos_insumos_services import servListProduIsum, servAddProduIsum, servDelProduIsum, servModProduIsum

def cntListProduIsum():
    data = servListProduIsum()
    return jsonify(data), 200

def cntAddProduIsum():
    data = servAddProduIsum()
    return jsonify(data), 200

def cntDelProduIsum():
    data = servDelProduIsum()
    return jsonify(data), 200

def cntModProduIsum():
    data = servModProduIsum()
    return jsonify(data), 201

