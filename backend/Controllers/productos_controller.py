from flask import jsonify, request
from Services.productos_services import servListProductos, servAddProductos, servDelProductos, servModProductos

def cntListProductos():
    data = servListProductos()
    return jsonify(data), 200

def cntAddProductos():
    data = servAddProductos()
    return jsonify(data), 200

def cntDelProductos():
    data = servDelProductos()
    return jsonify(data), 200

def cntModProdutos():
    data = servModProductos()
    return jsonify(data), 201
