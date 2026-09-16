from flask import Blueprint
from Controllers.productos_controller import cntListProductos, cntAddProductos, cntDelProductos, cntModProductos, cntGetProductos

productos_bp = Blueprint('productos_bp', __name__)

@productos_bp.route('/', methods=['GET'])
def listProductos():
    x = cntListProductos()
    return x

@productos_bp.route('/<int:id>', methods=['GET'])
def getProductos(id):
    return cntGetProductos(id)

@productos_bp.route('/', methods=['POST'])
def createProductos():
    x = cntAddProductos()
    return x

@productos_bp.route('/<int:id>', methods=['PUT'])
def updateProductos(id):
    x = cntModProductos(id)
    return x

@productos_bp.route('/<int:id>', methods=['DELETE'])
def deleteProductos(id):
    x = cntDelProductos(id)
    return x