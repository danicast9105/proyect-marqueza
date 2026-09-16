from flask import jsonify, request
from Services.vent_prod_services import (
    servListVentProd,
    addVentProd,
    deleteVentProd,
    updateVentProd
)
from Services.vent_prod_services import servListVentProd, getVentProd, addVentProd, deleteVentProd, updateVentProd

class vent_prod_controller:

    def cntListVentProd():
        data = servListVentProd()
        return jsonify(data), 200

    def cntAddVentProd():
        # Validar que el cuerpo de la petición exista
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        cantidad = data.get("cantidad")
        vent_id = data.get("vent_id")
        prod_id = data.get("prod_id")
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

        # Validar campos obligatorios
        if cantidad is None or vent_id is None or prod_id is None:
            return jsonify({
                "error": "Los campos 'cantidad', 'vent_id' y 'prod_id' son obligatorios"
            }), 400

        # Validar cantidad
        try:
            cantidad = int(cantidad)
            if cantidad < 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'cantidad' debe ser un entero mayor 0"}), 400

        # Validar vent_id
        try:
            vent_id = int(vent_id)
            if vent_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'vent_id' debe ser un entero positivo"}), 400

        # Validar prod_id
        try:
            prod_id = int(prod_id)
            if prod_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'prod_id' debe ser un entero positivo"}), 400

        # Llamar al servicio
        x = addVentProd(cantidad, vent_id, prod_id)
        return jsonify(x), 200

    def cntDelVentProd():
        data = deleteVentProd()
        return jsonify(data), 200

    def cntModVentProd():
        # Validar que el cuerpo de la petición exista
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        id = data.get("id")
        cantidad = data.get("cantidad")
        vent_id = data.get("vent_id")
        prod_id = data.get("prod_id")

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
        if cantidad is None and vent_id is None and prod_id is None:
            return jsonify({"error": "Debes enviar al menos un campo para actualizar"}), 400

        # Validar cantidad
        if cantidad is not None:
            try:
                cantidad = int(cantidad)
                if cantidad < 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'cantidad' debe ser un entero mayor o igual a 0"}), 400

        # Validar vent_id 
        if vent_id is not None:
            try:
                vent_id = int(vent_id)
                if vent_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'vent_id' debe ser un entero positivo"}), 400

        # Validar prod_id 
        if prod_id is not None:
            try:
                prod_id = int(prod_id)
                if prod_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'prod_id' debe ser un entero positivo"}), 400

        # Llamar al servicio
        x = updateVentProd(id, cantidad, vent_id, prod_id)
        return jsonify(x), 201
