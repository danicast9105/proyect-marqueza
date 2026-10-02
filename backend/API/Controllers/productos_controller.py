from flask import jsonify, request

from Services.productos_services import (addProductos, deleteProductos,
                                         servListProductos, updateProductos)
from Controllers.response_helpers import request_id, request_object

class productos_controller:
    def cntListProductos():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        return jsonify(servListProductos(id)), 200

    def cntAddProductos():
        data, error = request_object()
        if error:
            return error
        payload, status = addProductos(data)
        return jsonify(payload), status

    def cntDelProductos(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        payload, status = deleteProductos(id)
        return jsonify(payload), status

    def cntModProductos(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error
        payload, status = updateProductos(id, data)
        return jsonify(payload), status
