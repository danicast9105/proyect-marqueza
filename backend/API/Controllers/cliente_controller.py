from flask import jsonify, request
from Services.cliente_services import cliente_services

class cliente_controller:
    def cntListCliente():
        data = cliente_services.servListCliente()
        return jsonify(data), 200

    def cntAddCliente():
        persona_id = request.json["persona_id"]

        data = cliente_services.addCliente(persona_id)
        return jsonify(data), 200

    def cntDelCliente(id):
        data = cliente_services.deleteCliente(id)
        return jsonify(data), 200

    def cntModCliente(id):
        persona_id = request.json["persona_id"]

        data = cliente_services.updateCliente(id, persona_id)
        return jsonify(data), 200

