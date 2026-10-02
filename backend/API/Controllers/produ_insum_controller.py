from flask import jsonify, request
from Services.produ_insum_services import produ_insum_services
from Controllers.response_helpers import controller_response, request_id, request_object

class produ_insum_controller:
    def cntListProduInsum():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data = produ_insum_services.servListProduInsum(id)
        return jsonify(data), 200

    def cntAddProduInsum():
        data, error = request_object()
        if error:
            return error
        cantidad = data.get("cantidad")
        producto_id = data.get("producto_id")
        insumo_id = data.get("insumo_id")
        x = produ_insum_services.addProduInsum(cantidad, producto_id, insumo_id)
        return controller_response(x)

    def cntDelProduInsum(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data = produ_insum_services.deleteProduInsum(id)
        return controller_response(data)

    def cntModProduInsum(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error
        cantidad = data.get("cantidad")
        producto_id = data.get("producto_id")
        insumo_id = data.get("insumo_id")
        x = produ_insum_services.updateProduInsum(id, cantidad, producto_id, insumo_id)
        return controller_response(x)
