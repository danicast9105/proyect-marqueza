from flask import jsonify, request

from Services.recuperacion_contrasena_services import (
    recuperacion_contrasena_services)
from Controllers.response_helpers import request_id, request_object


class recuperacion_contrasena_controller:
    def cntListRecuperacion():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        return jsonify(recuperacion_contrasena_services.servListRecuperacion(id)), 200

    def cntAddRecuperacion():
        data, error = request_object()
        if error:
            return error
        payload, status = recuperacion_contrasena_services.addRecuperacionContrasena(
            data
        )
        return jsonify(payload), status

    def cntDelRecuperacion(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        payload, status = recuperacion_contrasena_services.deleteRecuperacionContrasena(id)
        return jsonify(payload), status

    def cntModRecuperacion(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error
        payload, status = recuperacion_contrasena_services.updateRecuperacionContrasena(
            id, data
        )
        return jsonify(payload), status
