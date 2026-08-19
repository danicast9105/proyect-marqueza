from flask import jsonify, request
from Services.ventas_productos_services import servListVentProd, servAddVentProd, servDelVentProd, servModVentProd

def cntListVentProd():
    data = servListVentProd()
    return jsonify(data), 200

def cntAddVentProd():
    data = servAddVentProd()
    return jsonify(data), 200

def cntDelVentProd():
    data = servDelVentProd()
    return jsonify(data), 200

def cntModVentProd():
    data = servModVentProd()
    return jsonify(data), 201

