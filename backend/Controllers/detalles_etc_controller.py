from flask import jsonify, request
from Services.detalles_etc_services import servListDetallesEtc, servAddDetallesEtc, servDelDetallesEtc, servModDetallesEtc

def cntListDetallesEtc():
    data = servListDetallesEtc()
    return jsonify(data), 200

def cntAddCliente():
    data = servAddDetallesEtc()
    return jsonify(data), 200

def cntDelCliente():
    data = servDelDetallesEtc()
    return jsonify(data), 200

def cntModCliente():
    data = servModDetallesEtc()
    return jsonify(data), 201

