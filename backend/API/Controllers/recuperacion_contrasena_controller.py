from flask import jsonify, request

from Services.recuperacion_contrasena_services import (
    recuperacion_contrasena_services)


class recuperacion_contrasena_controller:
    @staticmethod
    def cntListRecuperacion():
        return jsonify(recuperacion_contrasena_services.servListRecuperacion()), 200

    @staticmethod
    def cntAddRecuperacion():
        payload, status = recuperacion_contrasena_services.addRecuperacionContrasena(
            request.get_json(silent=True) or {}
        )
        return jsonify(payload), status

    @staticmethod
    def cntDelRecuperacion(id):
        payload, status = recuperacion_contrasena_services.deleteRecuperacionContrasena(id)
        return jsonify(payload), status

    @staticmethod
    def cntModRecuperacion(id):
        payload, status = recuperacion_contrasena_services.updateRecuperacionContrasena(
            id, request.get_json(silent=True) or {}
        )
        return jsonify(payload), status
