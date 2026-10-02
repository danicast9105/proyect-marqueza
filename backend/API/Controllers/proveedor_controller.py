from flask import jsonify, request

from Services.proveedor_services import (addProveedor, deleteProveedor,
                                         servListProveedor, updateProveedor)
from Controllers.response_helpers import request_id, request_object

class proveedor_controller:
    def cntListProveedor():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        return jsonify(servListProveedor(id)), 200

    def cntAddProveedor():
        data, error = request_object()
        if error:
            return error
        payload, status = addProveedor(data)
        return jsonify(payload), status

    def cntDelProveedor(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        payload, status = deleteProveedor(id)
        return jsonify(payload), status

    def cntModProveedor(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error
        payload, status = updateProveedor(id, data)
        return jsonify(payload), status
