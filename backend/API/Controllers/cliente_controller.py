from flask import jsonify, request

from Services.cliente_services import cliente_services


class cliente_controller:
    @staticmethod
    def cntListCliente():
        return jsonify(cliente_services.servListCliente()), 200

    @staticmethod
    def cntAddCliente():
        data = request.get_json(silent=True) or {}
        payload, status = cliente_services.addCliente(data)
        return jsonify(payload), status

    @staticmethod
    def cntDelCliente(id):
        payload, status = cliente_services.deleteCliente(id)
        return jsonify(payload), status

    @staticmethod
    def cntModCliente(id):
        data = request.get_json(silent=True) or {}
        payload, status = cliente_services.updateCliente(id, data)
        return jsonify(payload), status
