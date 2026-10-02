from flask import jsonify, request
from Services.detalles_etc_services import detalles_etc_services
from Controllers.response_helpers import (
    controller_response, request_id, request_object,
)

class detalles_etc_controller:
    def cntListDetalles_etc():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data = detalles_etc_services.servListDetalles_etc(id)
        return jsonify(data), 200

    def cntAddDetalles_etc():
        data, error = request_object()
        if error:
            return error

        det_etc_nombre = data.get("det_etc_nombre")
        det_etc_etc_id = data.get("det_etc_etc_id")
        det_etc_per_id = data.get("det_etc_per_id")

        x = detalles_etc_services.addDetalles_etc(det_etc_nombre, det_etc_etc_id, det_etc_per_id)
        return controller_response(x)

    def cntDelDetalles_etc(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data = detalles_etc_services.deleteDetalles_etc(id)
        return controller_response(data)

    def cntModDetalles_etc(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error

        det_etc_nombre = data.get("det_etc_nombre")
        det_etc_etc_id = data.get("det_etc_etc_id")
        det_etc_per_id = data.get("det_etc_per_id")

        x = detalles_etc_services.updateDetalles_etc(id, det_etc_nombre, det_etc_etc_id, det_etc_per_id)
        return controller_response(x)
