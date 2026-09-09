from flask import jsonify, request
from Services.ventas_services import servListVentas, addVentas, deleteVentas, updateVentas

def cntListVentas():
    data = servListVentas()
    return jsonify(data), 200

def cntAddVentas():
    data = addVentas()
    return jsonify(data), 200

def cntDelVentas():
    data = deleteVentas()
    return jsonify(data), 200

def cntModVentas():
    data = updateVentas()
    return jsonify(data), 201

