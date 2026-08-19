from flask import Blueprint
from Controllers.producto_insumo_controller import cntListProductoInsumos, cntCreateProductoInsumo, cntUpdateProductoInsumo, cntDeleteProductoInsumo

producto_insumo_bp = Blueprint('producto_insumo_bp', __name__)

@producto_insumo_bp.route('/', methods=['GET'])
def listProductoInsumos():
    return cntListProductoInsumos()

@producto_insumo_bp.route('/create', methods=['POST'])
def createProductoInsumo():
    return cntCreateProductoInsumo()

@producto_insumo_bp.route('/edit', methods=['PUT'])
def updateProductoInsumo():
    return cntUpdateProductoInsumo()

@producto_insumo_bp.route('/delete', methods=['DELETE'])
def deleteProductoInsumo():
    return cntDeleteProductoInsumo()

# http://127.0.0.1:5000/producto_insumos/
# http://127.0.0.1:5000/producto_insumos/create
# http://127.0.0.1:5000/producto_insumos/edit
# http://127.0.0.1:5000/producto_insumos/delete