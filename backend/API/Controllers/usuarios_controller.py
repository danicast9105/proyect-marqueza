from flask import jsonify, request

from Services.usuarios_services import (addUsuarios, deleteUsuarios,
                                        servListUsuarios, updateUsuarios)


def cntListUsuarios():
    return jsonify(servListUsuarios()), 200


def cntAddUsuarios():
    payload, status = addUsuarios(request.get_json(silent=True) or {})
    return jsonify(payload), status


def cntDelUsuarios(id):
    payload, status = deleteUsuarios(id)
    return jsonify(payload), status


def cntModUsuarios(id):
    payload, status = updateUsuarios(id, request.get_json(silent=True) or {})
    return jsonify(payload), status
