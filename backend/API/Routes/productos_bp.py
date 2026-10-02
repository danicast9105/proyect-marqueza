from flask import Blueprint, jsonify
from Controllers.productos_controller import productos_controller

productos_bp = Blueprint('productos_bp', __name__)

@productos_bp.route('/', methods=['GET'])
def listProductos():
    x = productos_controller.cntListProductos()
    return x

@productos_bp.route('/', methods=['POST'])
def createProductos():
    x = productos_controller.cntAddProductos()
    return x

@productos_bp.route('/<id>', methods=['PUT'])
def updateProductos(id):
    x = productos_controller.cntModProductos(id)
    return x

@productos_bp.route('/<id>', methods=['DELETE'])
def deleteProductos(id):
    x = productos_controller.cntDelProductos(id)
    return x
