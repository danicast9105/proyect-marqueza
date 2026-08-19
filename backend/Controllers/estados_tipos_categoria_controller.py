from flask import jsonify, request
from Services.estados_tipos_categoria_services import servListEstadosTiposCategoria, servAddEstadosTiposCategoria, servDelEstadosTipoCategoria, servModEstadosTiposCategoria

def cntListEstadosTiposCategoria():
    data = servListEstadosTiposCategoria()
    return jsonify(data), 200

def cntAddEstadosTiposCategoria():
    data = servAddEstadosTiposCategoria()
    return jsonify(data), 200

def cntDelEstadosTiposCategoria():
    data = servDelEstadosTipoCategoria()
    return jsonify(data), 200

def cntModEstadosTiposCategoria():
    data = servModEstadosTiposCategoria()
    return jsonify(data), 201

