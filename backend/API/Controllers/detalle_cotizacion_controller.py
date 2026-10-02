from flask import jsonify, request

from Services.detalle_cotizacion_services import detalle_cotizacion_services
from Controllers.response_helpers import (
    controller_response, request_id, request_object,
)


class detalle_cotizacion_controller:
    def cntListDetalleCotizacion():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        return jsonify(detalle_cotizacion_services.servListDetalleCotizacion(id)), 200

    def cntAddDetalleCotizacion():
        data, error = request_object()
        if error:
            return error
        return controller_response(
            detalle_cotizacion_services.addDetalleCotizacion(data), 201
        )

    def cntDelDetalleCotizacion(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        return controller_response(detalle_cotizacion_services.deleteDetalleCotizacion(id))

    def cntModDetalleCotizacion(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error
        return controller_response(
            detalle_cotizacion_services.updateDetalleCotizacion(id, data)
        )
