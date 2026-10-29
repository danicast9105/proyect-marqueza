from flask import jsonify, request
from Services.proveedor_services import (
    servListProveedor,
    getProveedor,
    addProveedor,
    deleteProveedor,
    updateProveedor
)
from Controllers.request_validation import obtener_campos_faltantes


def cntListProveedor():
    return jsonify(servListProveedor()), 200


def cntGetProveedor(id):
    data = getProveedor(id)
    if data is None:
        return jsonify({"error": "Proveedor no encontrado"}), 404
    return jsonify(data), 200


def cntAddProveedor():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "El cuerpo debe ser un objeto JSON"}), 400

    campos_requeridos = ("per_id",)
    campos_faltantes = obtener_campos_faltantes(data, campos_requeridos)
    if campos_faltantes:
        return jsonify({
            "error": "Faltan campos obligatorios",
            "campos_faltantes": campos_faltantes
        }), 400

    try:
        per_id = int(data["per_id"])
        if per_id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El campo 'per_id' debe ser un entero positivo"}), 400

    return jsonify(addProveedor(per_id)), 200


def cntDelProveedor(id):
    return jsonify(deleteProveedor(id)), 200


def cntModProveedor(id):
    try:
        id = int(id)
        if id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El ID debe ser un entero positivo"}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "El cuerpo debe ser un objeto JSON"}), 400

    campos_requeridos = ("per_id",)
    campos_faltantes = obtener_campos_faltantes(data, campos_requeridos)
    if campos_faltantes:
        return jsonify({
            "error": "Faltan campos obligatorios",
            "campos_faltantes": campos_faltantes
        }), 400

    try:
        per_id = int(data["per_id"])
        if per_id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El campo 'per_id' debe ser un entero positivo"}), 400

    return jsonify(updateProveedor(id, per_id)), 200
