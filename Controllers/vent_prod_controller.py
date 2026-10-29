from flask import jsonify, request
from Services.vent_prod_services import (
    servListVentProd,
    getVentProd,
    addVentProd,
    deleteVentProd,
    updateVentProd
)
from Controllers.request_validation import obtener_campos_faltantes


def cntListVentProd():
    return jsonify(servListVentProd()), 200


def cntGetVentProd(id):
    data = getVentProd(id)
    if data is None:
        return jsonify({"error": "Relación venta-producto no encontrada"}), 404
    return jsonify(data), 200


def cntAddVentProd():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "El cuerpo debe ser un objeto JSON"}), 400

    campos_requeridos = ("cantidad", "vent_id", "prod_id")
    campos_faltantes = obtener_campos_faltantes(data, campos_requeridos)
    if campos_faltantes:
        return jsonify({
            "error": "Faltan campos obligatorios",
            "campos_faltantes": campos_faltantes
        }), 400

    cantidad = data["cantidad"]
    try:
        cantidad = int(cantidad)
        if cantidad < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El campo 'cantidad' debe ser un entero mayor o igual a 0"}), 400

    try:
        vent_id = int(data["vent_id"])
        if vent_id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El campo 'vent_id' debe ser un entero positivo"}), 400

    try:
        prod_id = int(data["prod_id"])
        if prod_id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El campo 'prod_id' debe ser un entero positivo"}), 400

    return jsonify(addVentProd(cantidad, vent_id, prod_id)), 200


def cntDelVentProd(id):
    return jsonify(deleteVentProd(id)), 200


def cntModVentProd(id):
    try:
        id = int(id)
        if id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El ID debe ser un entero positivo"}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "El cuerpo debe ser un objeto JSON"}), 400

    campos = ("cantidad", "vent_id", "prod_id")
    if all(data.get(campo) is None for campo in campos):
        return jsonify({"error": "Debes enviar al menos un campo para actualizar"}), 400

    cantidad = data.get("cantidad")
    vent_id = data.get("vent_id")
    prod_id = data.get("prod_id")

    if cantidad is not None:
        try:
            cantidad = int(cantidad)
            if cantidad < 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'cantidad' debe ser un entero mayor o igual a 0"}), 400

    if vent_id is not None:
        try:
            vent_id = int(vent_id)
            if vent_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'vent_id' debe ser un entero positivo"}), 400

    if prod_id is not None:
        try:
            prod_id = int(prod_id)
            if prod_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'prod_id' debe ser un entero positivo"}), 400

    return jsonify(updateVentProd(id, cantidad, vent_id, prod_id)), 200
