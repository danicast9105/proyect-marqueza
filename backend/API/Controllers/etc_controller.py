from flask import jsonify, request
from Services.etc_services import etc_services
from Controllers.response_helpers import (
    controller_response, request_id, request_object,
)

class etc_controller:
    def cntListETC():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data = etc_services.servListETC(id)
        return jsonify(data), 200

    def cntAddETC():
        data, error = request_object()
        if error:
            return error

        etc_nombre = data.get("etc_nombre")
        x = etc_services.addETC(etc_nombre)
        return controller_response(x)

    def cntDelETC(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data = etc_services.deleteETC(id)
        return controller_response(data)

    def cntModETC(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error

        etc_nombre = data.get("etc_nombre")
        x = etc_services.updateETC(id, etc_nombre)
        return controller_response(x)
