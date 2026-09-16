from flask import jsonify, request
from Services.productos_services import servListProductos, getProductos, addProductos, deleteProductos, updateProductos

def cntListProductos():
    data = servListProductos()
    return jsonify(data), 200

def cntGetProductos(id):
    data = getProductos(id)
    if data is None:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(data), 200

def cntAddProductos():
    data = request.get_json(silent=True) or {}
    fields = ("codigo", "nombre", "cantidad", "precio", "estado", "usua_id", "det_etc_id")
    if any(field not in data for field in fields):
        return jsonify({"error": "Todos los campos del producto son obligatorios"}), 400
    result = addProductos(*(data[field] for field in fields))
    return jsonify(result), 201

def cntDelProductos(id):
    data = deleteProductos(id)
    return jsonify(data), 200

def cntModProductos(id):
    data = request.get_json(silent=True) or {}
    fields = ("codigo", "nombre", "cantidad", "precio", "estado", "usua_id", "det_etc_id")
    if any(field not in data for field in fields):
        return jsonify({"error": "Todos los campos del producto son obligatorios"}), 400
    result = updateProductos(id, *(data[field] for field in fields))
    return jsonify(result), 200

