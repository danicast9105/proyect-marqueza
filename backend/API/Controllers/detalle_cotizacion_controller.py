from flask import jsonify, request

from Services.detalle_cotizacion_services import detalle_cotizacion_services


class detalle_cotizacion_controller:
    @staticmethod
    def cntListDetalleCotizacion():
        return jsonify(detalle_cotizacion_services.servListDetalleCotizacion()), 200

    @staticmethod
    def cntAddDetalleCotizacion():
        return jsonify(detalle_cotizacion_services.addDetalleCotizacion()), 201

    @staticmethod
    def cntDelDetalleCotizacion(id):
        return jsonify(detalle_cotizacion_services.deleteDetalleCotizacion(id)), 200

    @staticmethod
    def cntModDetalleCotizacion(id):
        return jsonify(detalle_cotizacion_services.updateDetalleCotizacion(id)), 200
