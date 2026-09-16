from flask import jsonify, request
from Services.proveedor_services import servListProveedor, getProveedor, addProveedor, deleteProveedor, updateProveedor

def cntListProveedor():
    data = servListProveedor()
    return jsonify(data), 200

def cntGetProveedor(id):
    data = getProveedor(id)
    if data is None:
        return jsonify({"error": "Proveedor no encontrado"}), 404
    return jsonify(data), 200

def cntAddProveedor():
    data = request.get_json(silent=True) or {}
    if "per_id" not in data:
        return jsonify({"error": "El campo 'per_id' es obligatorio"}), 400
    return jsonify(addProveedor(data["per_id"])), 201

def cntDelProveedor(id):
    data = deleteProveedor(id)
    return jsonify(data), 200

def cntModProveedor(id):
    data = request.get_json(silent=True) or {}
    if "per_id" not in data:
        return jsonify({"error": "El campo 'per_id' es obligatorio"}), 400
    return jsonify(updateProveedor(id, data["per_id"])), 200

