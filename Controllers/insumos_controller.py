from flask import jsonify, request
from Services.insumos_services import servListInsumos, addInsumos, deleteInsumos, updateInsumos

def cntListInsumos():
    data = servListInsumos()
    return jsonify(data), 200

def cntAddInsumos():
    data = addInsumos()
    return jsonify(data), 200

def cntDelInsumos():
    data = deleteInsumos()
    return jsonify(data), 200

def cntModInsumos():
    data = updateInsumos()
    return jsonify(data), 201

