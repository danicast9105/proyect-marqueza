from flask import jsonify, request

from Services.bitacora_auditoria_services import bitacora_auditoria_services


class bitacora_auditoria_controller:
    @staticmethod
    def cntListBitacora():
        return jsonify(bitacora_auditoria_services.servListBitacora()), 200

    @staticmethod
    def cntAddBitacora():
        payload, status = bitacora_auditoria_services.addBitacoraAuditoria(
            request.get_json(silent=True) or {}
        )
        return jsonify(payload), status

    @staticmethod
    def cntDelBitacora(id):
        payload, status = bitacora_auditoria_services.deleteBitacoraAuditoria(id)
        return jsonify(payload), status

    @staticmethod
    def cntModBitacora(id):
        payload, status = bitacora_auditoria_services.updateBitacoraAuditoria(
            id, request.get_json(silent=True) or {}
        )
        return jsonify(payload), status
