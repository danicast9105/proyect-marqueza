from flask import jsonify, request

from Services.proveedor_services import (addProveedor, deleteProveedor,
                                         servListProveedor, updateProveedor)


def cntListProveedor():
    return jsonify(servListProveedor()), 200


def cntAddProveedor():
    payload, status = addProveedor(request.get_json(silent=True) or {})
    return jsonify(payload), status


def cntDelProveedor(id):
    payload, status = deleteProveedor(id)
    return jsonify(payload), status


def cntModProveedor(id):
    payload, status = updateProveedor(id, request.get_json(silent=True) or {})
    return jsonify(payload), status
