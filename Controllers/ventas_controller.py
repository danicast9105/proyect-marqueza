from flask import jsonify, request
from Services.ventas_services import servListVentas, getVentas, addVentas, deleteVentas, updateVentas

def cntListVentas():
    data = servListVentas()
    return jsonify(data), 200

def cntGetVentas(id):
    data = getVentas(id)
    if data is None:
        return jsonify({"error": "Venta no encontrada"}), 404
    return jsonify(data), 200

def cntAddVentas():
    data = request.get_json(silent=True) or {}
    fields = ("fecha", "usua_id", "cli_id")
    if any(field not in data for field in fields):
        return jsonify({"error": "Los campos fecha, usua_id y cli_id son obligatorios"}), 400
    return jsonify(addVentas(*(data[field] for field in fields))), 201

def cntDelVentas(id):
    data = deleteVentas(id)
    return jsonify(data), 200

def cntModVentas(id):
    data = request.get_json(silent=True) or {}
    fields = ("fecha", "usua_id", "cli_id")
    if any(field not in data for field in fields):
        return jsonify({"error": "Los campos fecha, usua_id y cli_id son obligatorios"}), 400
    return jsonify(updateVentas(id, *(data[field] for field in fields))), 200

