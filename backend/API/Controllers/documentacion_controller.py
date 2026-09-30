from flask import jsonify, request

from Services.documentacion_services import documentacion_services


class documentacion_controller:
    @staticmethod
    def cntListDocumentacion():
        payload, status = documentacion_services.servListDocumentacion(), 200
        return jsonify(payload), status

    @staticmethod
    def cntAddDocumentacion():
        data = request.get_json(silent=True) or {}
        payload, status = documentacion_services.addDocumentacion(
            data.get("tipo", ""), data.get("titulo", ""), data.get("descripcion", ""),
            data.get("ruta", ""), data.get("activo", True),
        )
        return jsonify(payload), status

    @staticmethod
    def cntDelDocumentacion(id):
        payload, status = documentacion_services.deleteDocumentacion(id)
        return jsonify(payload), status

    @staticmethod
    def cntModDocumentacion(id):
        data = request.get_json(silent=True) or {}
        payload, status = documentacion_services.updateDocumentacion(
            id, data.get("tipo", ""), data.get("titulo", ""), data.get("descripcion", ""),
            data.get("ruta", ""), data.get("activo", True),
        )
        return jsonify(payload), status
