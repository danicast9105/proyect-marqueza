from flask import jsonify, request
from Services.detalles_etc_services import servListDetalles_etc, addDetalles_etc, deleteDetalles_etc, updateDetalles_etc

def cntListDetalles_etc():
    data = servListDetalles_etc()
    return jsonify(data), 200

def cntAddDetalles_etc():
    data = addDetalles_etc()
    return jsonify(data), 200

def cntDelDetalles_etc():
    data = deleteDetalles_etc()
    return jsonify(data), 200

def cntModDetalles_etc():
    data = updateDetalles_etc()
    return jsonify(data), 201

