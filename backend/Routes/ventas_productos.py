from flask import Blueprint
from Controllers.venta_producto_controller import cntListVentaProductos, cntCreateVentaProducto, cntUpdateVentaProducto, cntDeleteVentaProducto

venta_producto_bp = Blueprint('venta_producto_bp', __name__)

@venta_producto_bp.route('/', methods=['GET'])
def listVentaProductos():
    return cntListVentaProductos()

@venta_producto_bp.route('/create', methods=['POST'])
def createVentaProducto():
    return cntCreateVentaProducto()

@venta_producto_bp.route('/edit', methods=['PUT'])
def updateVentaProducto():
    return cntUpdateVentaProducto()

@venta_producto_bp.route('/delete', methods=['DELETE'])
def deleteVentaProducto():
    return cntDeleteVentaProducto()

# http://127.0.0.1:5000/venta_productos/
# http://127.0.0.1:5000/venta_productos/create
# http://127.0.0.1:5000/venta_productos/edit
# http://127.0.0.1:5000/venta_productos/delete