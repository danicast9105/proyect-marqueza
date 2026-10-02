from flask import jsonify, request

from Services.cliente_services import cliente_services
from Controllers.response_helpers import request_id, request_object


class cliente_controller:
    def cntListCliente():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        return jsonify(cliente_services.servListCliente(id)), 200

    def cntAddCliente():
        data, error = request_object()
        if error:
            return error
        payload, status = cliente_services.addCliente(data)
        return jsonify(payload), status

    def cntDelCliente(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        payload, status = cliente_services.deleteCliente(id)
        return jsonify(payload), status

    def cntModCliente(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error
        payload, status = cliente_services.updateCliente(id, data)
        return jsonify(payload), status
