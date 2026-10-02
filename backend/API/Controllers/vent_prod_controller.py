from flask import jsonify, request
from Services.vent_prod_services import servListVentProd, addVentProd, deleteVentProd, updateVentProd
from Controllers.response_helpers import (
    controller_response, request_id, request_object,
)

class vent_prod_controller:
    def cntListVentProd():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data = servListVentProd(id)
        return jsonify(data), 200

    def cntAddVentProd():
        data, error = request_object()
        if error:
            return error
        data = addVentProd(data)
        return controller_response(data)

    def cntDelVentProd(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data = deleteVentProd(id)
        return controller_response(data)

    def cntModVentProd(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        body, error = request_object()
        if error:
            return error
        data = updateVentProd(id, body)
        return controller_response(data, 201)
