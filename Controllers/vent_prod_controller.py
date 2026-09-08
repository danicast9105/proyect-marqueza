from flask import jsonify, request
from Services.vent_prod_services import servListVentProd, addVentProd, deleteVentProd, updateVentProd

def cntListVentProd():
    data = servListVentProd()
    return jsonify(data), 200

def cntAddVentProd():
    data = addVentProd()
    return jsonify(data), 200

def cntDelVentProd():
    data = deleteVentProd()
    return jsonify(data), 200

def cntModVentProd():
    data = updateVentProd()
    return jsonify(data), 201

