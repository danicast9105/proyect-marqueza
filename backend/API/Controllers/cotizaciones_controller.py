from flask import jsonify, request

from Services.cotizaciones_services import (addCotizaciones,
                                            deleteCotizaciones,
                                            servListCotizaciones,
                                            updateCotizaciones)


class cotizaciones_controller:
    @staticmethod
    def cntListCotizaciones():
        return jsonify(servListCotizaciones()), 200

    @staticmethod
    def cntAddCotizaciones():
        payload, status = addCotizaciones(request.get_json(silent=True) or {})
        return jsonify(payload), status

    @staticmethod
    def cntDelCotizaciones(id):
        payload, status = deleteCotizaciones(id)
        return jsonify(payload), status

    @staticmethod
    def cntModCotizaciones(id):
        payload, status = updateCotizaciones(id, request.get_json(silent=True) or {})
        return jsonify(payload), status
