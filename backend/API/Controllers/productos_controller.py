from flask import jsonify, request
from Services.productos_services import servListProductos, addProductos, deleteProductos, updateProductos

def cntListProductos():
    data = servListProductos()
    return jsonify(data), 200

def cntAddProductos():
    data = addProductos()
    return jsonify(data), 200

def cntDelProductos():
    data = deleteProductos()
    return jsonify(data), 200

def cntModProductos():
    data = updateProductos()
    return jsonify(data), 201

