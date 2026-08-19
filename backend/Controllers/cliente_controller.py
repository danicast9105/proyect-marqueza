from flask import jsonify, request
from Services.cliente_services import servListCliente, servAddCliente, servDelCliente, servModCliente

def cntListCliente():
    data = servListCliente()
    return jsonify(data), 200

def cntAddCliente():
    data = servAddCliente()
    return jsonify(data), 200

def cntDelCliente():
    data = servDelCliente()
    return jsonify(data), 200

def cntModCliente():
    data = servModCliente()
    return jsonify(data), 201

