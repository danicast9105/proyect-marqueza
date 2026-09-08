from flask import jsonify, request
from Services.proveedor_services import servListProveedor, addProveedor, deleteProveedor, updateProveedor

def cntListProveedor():
    data = servListProveedor()
    return jsonify(data), 200

def cntAddProveedor():
    data = addProveedor()
    return jsonify(data), 200

def cntDelProveedor():
    data = deleteProveedor()
    return jsonify(data), 200

def cntModProveedor():
    data = updateProveedor()
    return jsonify(data), 201

