from flask import jsonify, request
from datetime import datetime
from Services.ventas_services import (
    servListVentas,
    addVentas,
    deleteVentas,
    updateVentas
)
from Services.ventas_services import servListVentas, getVentas, addVentas, deleteVentas, updateVentas

class ventas_controller:
    def cntListVentas():
        data = servListVentas()
        return jsonify(data), 200

    def cntAddVentas():
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        fecha = data.get("fecha")
        usuario_id = data.get("usuario_id")
        cliente_id = data.get("cliente_id")

        if fecha is None or usuario_id is None or cliente_id is None:
            return jsonify({
                "error": "Los campos 'fecha', 'usuario_id' y 'cliente_id' son obligatorios"
            }), 400
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

        # Validar fecha
        if not isinstance(fecha, str) or not fecha.strip():
            return jsonify({"error": "El campo 'fecha' debe ser una cadena no vacía"}), 400
        fecha = fecha.strip()

        # Validar usuario_id
        try:
            usuario_id = int(usuario_id)
            if usuario_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'usuario_id' debe ser un entero positivo"}), 400

        # Validar cliente_id
        try:
            cliente_id = int(cliente_id)
            if cliente_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'cliente_id' debe ser un entero positivo"}), 400

        x = addVentas(fecha, usuario_id, cliente_id)
        return jsonify(x), 200

    def cntDelVentas():
        data = deleteVentas()
        return jsonify(data), 200

    def cntModVentas():
        # Validar que el cuerpo de la petición exista
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        id = data.get("id")
        fecha = data.get("fecha")
        usuario_id = data.get("usuario_id")
        cliente_id = data.get("cliente_id")

        # Validar que el ID sea obligatorio
        if id is None:
            return jsonify({"error": "El campo 'id' es obligatorio"}), 400
        try:
            id = int(id)
            if id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'id' debe ser un entero positivo"}), 400

        # Verificar que al menos un campo llegue para actualizar
        if fecha is None and usuario_id is None and cliente_id is None:
            return jsonify({"error": "Debes enviar al menos un campo para actualizar"}), 400

        # Validar fecha
        if fecha is not None:
            if not isinstance(fecha, str) or not fecha.strip():
                return jsonify({"error": "El campo 'fecha' debe ser una cadena no vacía"}), 400
            fecha = fecha.strip()

        # Validar usuario_id
        if usuario_id is not None:
            try:
                usuario_id = int(usuario_id)
                if usuario_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'usuario_id' debe ser un entero positivo"}), 400

        # Validar cliente_id
        if cliente_id is not None:
            try:
                cliente_id = int(cliente_id)
                if cliente_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'cliente_id' debe ser un entero positivo"}), 400

        x = updateVentas(id, fecha, usuario_id, cliente_id)
        return jsonify(x), 201
