from flask import jsonify, request

from Services.bitacora_auditoria_services import bitacora_auditoria_services
from Controllers.response_helpers import request_id, request_object


class bitacora_auditoria_controller:
    def cntListBitacora():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        return jsonify(bitacora_auditoria_services.servListBitacora(id)), 200

    def cntAddBitacora():
        data, error = request_object()
        if error:
            return error
        payload, status = bitacora_auditoria_services.addBitacoraAuditoria(
            data
        )
        return jsonify(payload), status

    def cntDelBitacora(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        payload, status = bitacora_auditoria_services.deleteBitacoraAuditoria(id)
        return jsonify(payload), status

    def cntModBitacora(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error
        payload, status = bitacora_auditoria_services.updateBitacoraAuditoria(
            id, data
        )
        return jsonify(payload), status
