from flask import Blueprint
from Controllers.producto_controller import cntListProductos, cntCreateProducto, cntUpdateProducto, cntDeleteProducto

producto_bp = Blueprint('producto_bp', __name__)

@producto_bp.route('/', methods=['GET'])
def listProductos():
    return cntListProductos()

@producto_bp.route('/create', methods=['POST'])
def createProducto():
    return cntCreateProducto()

@producto_bp.route('/edit', methods=['PUT'])
def updateProducto():
    return cntUpdateProducto()

@producto_bp.route('/delete', methods=['DELETE'])
def deleteProducto():
    return cntDeleteProducto()

# http://127.0.0.1:5000/productos/
# http://127.0.0.1:5000/productos/create
# http://127.0.0.1:5000/productos/edit/<id>
# http://127.0.0.1:5000/productos/delete/<id>
