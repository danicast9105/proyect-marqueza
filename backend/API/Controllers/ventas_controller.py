from flask import jsonify, request

from Services.ventas_services import (addVentas, deleteVentas, servListVentas,
                                      updateVentas)


def cntListVentas():
    return jsonify(servListVentas()), 200


def cntAddVentas():
    payload, status = addVentas(request.get_json(silent=True) or {})
    return jsonify(payload), status


def cntDelVentas(id):
    payload, status = deleteVentas(id)
    return jsonify(payload), status


def cntModVentas(id):
    payload, status = updateVentas(id, request.get_json(silent=True) or {})
    return jsonify(payload), status
