from flask import jsonify, request
from Services.vent_prod_services import servListVentProd, addVentProd, deleteVentProd, updateVentProd

def cntListVentProd():
    data = servListVentProd()
    return jsonify(data), 200

def cntAddVentProd():
    data = addVentProd()
    return jsonify(data), 200

def cntDelVentProd(id):
    data = deleteVentProd(id)
    return jsonify(data), 200

def cntModVentProd(id):
    data = updateVentProd(id)
    return jsonify(data), 201
