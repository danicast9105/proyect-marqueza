from flask import jsonify, request
from Services.vent_prod_services import servListVentProd, getVentProd, addVentProd, deleteVentProd, updateVentProd

def cntListVentProd():
    data = servListVentProd()
    return jsonify(data), 200

def cntGetVentProd(id):
    data = getVentProd(id)
    if data is None:
        return jsonify({"error": "Relación venta-producto no encontrada"}), 404
    return jsonify(data), 200

def cntAddVentProd():
    data = request.get_json(silent=True) or {}
    fields = ("cantidad", "vent_id", "prod_id")
    if any(field not in data for field in fields):
        return jsonify({"error": "Los campos cantidad, vent_id y prod_id son obligatorios"}), 400
    return jsonify(addVentProd(*(data[field] for field in fields))), 201

def cntDelVentProd(id):
    data = deleteVentProd(id)
    return jsonify(data), 200

def cntModVentProd(id):
    data = request.get_json(silent=True) or {}
    fields = ("cantidad", "vent_id", "prod_id")
    if any(field not in data for field in fields):
        return jsonify({"error": "Los campos cantidad, vent_id y prod_id son obligatorios"}), 400
    return jsonify(updateVentProd(id, *(data[field] for field in fields))), 200

