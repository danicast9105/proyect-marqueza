from flask import jsonify, request

from Services.ventas_services import (addVentas, deleteVentas, servListVentas,
                                      updateVentas)
from Controllers.response_helpers import request_id, request_object

class ventas_controller:
    def cntListVentas():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        return jsonify(servListVentas(id)), 200

    def cntAddVentas():
        data, error = request_object()
        if error:
            return error
        payload, status = addVentas(data)
        return jsonify(payload), status

    def cntDelVentas(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        payload, status = deleteVentas(id)
        return jsonify(payload), status

    def cntModVentas(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error
        payload, status = updateVentas(id, data)
        return jsonify(payload), status
