from flask import jsonify, request
from Services.insumos_services import servListInsumos, servAddInsumos, servDelInsumos, servModInsumos

def cntListInsumos():
    data = servListInsumos()
    return jsonify(data), 200

def cntAddInsumos():
    data = servAddInsumos()
    return jsonify(data), 200

def cntDelInsumos():
    data = servDelInsumos()
    return jsonify(data), 200

def cntModInsumos():
    data = servModInsumos()
    return jsonify(data), 201

