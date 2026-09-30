from flask import jsonify, request

from Services.productos_services import (addProductos, deleteProductos,
                                         servListProductos, updateProductos)


def cntListProductos():
    return jsonify(servListProductos()), 200


def cntAddProductos():
    payload, status = addProductos(request.get_json(silent=True) or {})
    return jsonify(payload), status


def cntDelProductos(id):
    payload, status = deleteProductos(id)
    return jsonify(payload), status


def cntModProductos(id):
    payload, status = updateProductos(id, request.get_json(silent=True) or {})
    return jsonify(payload), status
