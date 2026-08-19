from flask import jsonify, request
from Services.proveedores_services import servListProveedores, servAddProveedores, servDelProveedores, servModProveedores

def cntListProveedores():
    data = servListProveedores()
    return jsonify(data), 200

def cntAddProveedores():
    data = servAddProveedores()
    return jsonify(data), 200

def cntDelProveedores():
    data = servDelProveedores()
    return jsonify(data), 200

def cntModProveedores():
    data = servModProveedores()
    return jsonify(data), 201

