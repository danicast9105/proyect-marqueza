from flask import jsonify, request

from Services.insumos_services import (addInsumos, deleteInsumos,
                                       servListInsumos, updateInsumos)
from Controllers.response_helpers import request_id, request_object


class insumos_controller:
    def cntListInsumos():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        return jsonify(servListInsumos(id)), 200

    def cntAddInsumos():
        data, error = request_object()
        if error:
            return error
        payload, status = addInsumos(data)
        return jsonify(payload), status

    def cntDelInsumos(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        payload, status = deleteInsumos(id)
        return jsonify(payload), status

    def cntModInsumos(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error
        payload, status = updateInsumos(id, data)
        return jsonify(payload), status
