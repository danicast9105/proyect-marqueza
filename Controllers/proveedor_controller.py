from flask import jsonify, request
from Services.proveedor_services import (
    servListProveedor,
    addProveedor,
    deleteProveedor,
    updateProveedor
)
from Services.proveedor_services import servListProveedor, getProveedor, addProveedor, deleteProveedor, updateProveedor

class proveedor_controller:
    def cntListProveedor():
        data = servListProveedor()
        return jsonify(data), 200

    def cntAddProveedor():
        # Validar que el cuerpo de la petición exista
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        per_id = data.get("per_id")

        # Validar campo obligatorio
        if per_id is None:
            return jsonify({"error": "El campo 'per_id' es obligatorio"}), 400
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

        # Validar per_id
        try:
            per_id = int(per_id)
            if per_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'per_id' debe ser un entero positivo"}), 400

        x = addProveedor(per_id)
        return jsonify(x), 200

    def cntDelProveedor():
        data = deleteProveedor()
        return jsonify(data), 200
    
    def cntModProveedor():
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        # Obtener campos
        id = data.get("id")
        per_id = data.get("per_id")

        # Validar que el ID sea obligatori
        if id is None:
            return jsonify({"error": "El campo 'id' es obligatorio"}), 400
        try:
            id = int(id)
            if id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'id' debe ser un entero positivo"}), 400

        # Validar que per_id sea obligatorio
        if per_id is None:
            return jsonify({"error": "El campo 'per_id' es obligatorio"}), 400
        try:
            per_id = int(per_id)
            if per_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'per_id' debe ser un entero positivo"}), 400

        x = updateProveedor(id, per_id)
        return jsonify(x), 201
