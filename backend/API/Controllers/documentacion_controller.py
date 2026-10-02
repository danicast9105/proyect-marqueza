from flask import jsonify, request

from Services.documentacion_services import documentacion_services
from Controllers.response_helpers import request_id, request_object


class documentacion_controller:
    def cntListDocumentacion():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        payload, status = documentacion_services.servListDocumentacion(id), 200
        return jsonify(payload), status

    def cntAddDocumentacion():
        data, error = request_object()
        if error:
            return error
        payload, status = documentacion_services.addDocumentacion(
            data.get("tipo", ""), data.get("titulo", ""), data.get("descripcion", ""),
            data.get("ruta", ""), data.get("activo", True),
        )
        return jsonify(payload), status

    def cntDelDocumentacion(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        payload, status = documentacion_services.deleteDocumentacion(id)
        return jsonify(payload), status

    def cntModDocumentacion(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error
        payload, status = documentacion_services.updateDocumentacion(
            id, data.get("tipo", ""), data.get("titulo", ""), data.get("descripcion", ""),
            data.get("ruta", ""), data.get("activo", True),
        )
        return jsonify(payload), status
