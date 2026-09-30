from flask import jsonify, request

from Services.insumos_services import (addInsumos, deleteInsumos,
                                       servListInsumos, updateInsumos)


class insumos_controller:
    @staticmethod
    def cntListInsumos():
        return jsonify(servListInsumos()), 200

    @staticmethod
    def cntAddInsumos():
        payload, status = addInsumos(request.get_json(silent=True) or {})
        return jsonify(payload), status

    @staticmethod
    def cntDelInsumos(id):
        payload, status = deleteInsumos(id)
        return jsonify(payload), status

    @staticmethod
    def cntModInsumos(id):
        payload, status = updateInsumos(id, request.get_json(silent=True) or {})
        return jsonify(payload), status
