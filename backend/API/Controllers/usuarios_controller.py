from flask import jsonify, request

from Services.usuarios_services import (addUsuarios, deleteUsuarios,
                                        servListUsuarios, updateUsuarios)
from Controllers.response_helpers import request_id, request_object

class usuarios_controller:
    def cntListUsuarios():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        return jsonify(servListUsuarios(id)), 200

    def cntAddUsuarios():
        data, error = request_object()
        if error:
            return error
        payload, status = addUsuarios(data)
        return jsonify(payload), status

    def cntDelUsuarios(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        payload, status = deleteUsuarios(id)
        return jsonify(payload), status

    def cntModUsuarios(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error
        payload, status = updateUsuarios(id, data)
        return jsonify(payload), status
