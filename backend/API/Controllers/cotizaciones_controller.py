from flask import jsonify, request

from Services.cotizaciones_services import (addCotizaciones,
                                            deleteCotizaciones,
                                            servListCotizaciones,
                                            updateCotizaciones)
from Controllers.response_helpers import request_id, request_object


class cotizaciones_controller:
    def cntListCotizaciones():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        return jsonify(servListCotizaciones(id)), 200

    def cntAddCotizaciones():
        data, error = request_object()
        if error:
            return error
        payload, status = addCotizaciones(data)
        return jsonify(payload), status

    def cntDelCotizaciones(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        payload, status = deleteCotizaciones(id)
        return jsonify(payload), status

    def cntModCotizaciones(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error
        payload, status = updateCotizaciones(id, data)
        return jsonify(payload), status
