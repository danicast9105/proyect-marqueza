from flask import jsonify, request
from Services.ventas_services import (
    servListVentas,
    getVentas,
    addVentas,
    deleteVentas,
    updateVentas
)
from Controllers.request_validation import obtener_campos_faltantes


def cntListVentas():
    return jsonify(servListVentas()), 200


def cntGetVentas(id):
    data = getVentas(id)
    if data is None:
        return jsonify({"error": "Venta no encontrada"}), 404
    return jsonify(data), 200


def cntAddVentas():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "El cuerpo debe ser un objeto JSON"}), 400

    campos_requeridos = ("fecha", "usuario_id", "cliente_id")
    campos_faltantes = obtener_campos_faltantes(data, campos_requeridos)
    if campos_faltantes:
        return jsonify({
            "error": "Faltan campos obligatorios",
            "campos_faltantes": campos_faltantes
        }), 400

    fecha = data["fecha"]
    if not isinstance(fecha, str) or not fecha.strip():
        return jsonify({"error": "El campo 'fecha' debe ser una cadena no vacía"}), 400

    try:
        usuario_id = int(data["usuario_id"])
        if usuario_id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El campo 'usuario_id' debe ser un entero positivo"}), 400

    try:
        cliente_id = int(data["cliente_id"])
        if cliente_id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El campo 'cliente_id' debe ser un entero positivo"}), 400

    return jsonify(addVentas(fecha.strip(), usuario_id, cliente_id)), 200


def cntDelVentas(id):
    return jsonify(deleteVentas(id)), 200


def cntModVentas(id):
    try:
        id = int(id)
        if id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El ID debe ser un entero positivo"}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "El cuerpo debe ser un objeto JSON"}), 400

    campos = ("fecha", "usuario_id", "cliente_id")
    if all(data.get(campo) is None for campo in campos):
        return jsonify({"error": "Debes enviar al menos un campo para actualizar"}), 400

    fecha = data.get("fecha")
    usuario_id = data.get("usuario_id")
    cliente_id = data.get("cliente_id")

    if fecha is not None:
        if not isinstance(fecha, str) or not fecha.strip():
            return jsonify({"error": "El campo 'fecha' debe ser una cadena no vacía"}), 400
        fecha = fecha.strip()

    if usuario_id is not None:
        try:
            usuario_id = int(usuario_id)
            if usuario_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'usuario_id' debe ser un entero positivo"}), 400

    if cliente_id is not None:
        try:
            cliente_id = int(cliente_id)
            if cliente_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'cliente_id' debe ser un entero positivo"}), 400

    return jsonify(updateVentas(id, fecha, usuario_id, cliente_id)), 200
