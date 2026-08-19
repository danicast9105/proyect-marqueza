from flask import Blueprint
from Controllers.venta_controller import cntListVentas, cntCreateVenta, cntUpdateVenta, cntDeleteVenta

venta_bp = Blueprint('venta_bp', __name__)

@venta_bp.route('/', methods=['GET'])
def listVentas():
    return cntListVentas()

@venta_bp.route('/create', methods=['POST'])
def createVenta():
    return cntCreateVenta()

@venta_bp.route('/edit', methods=['PUT'])
def updateVenta():
    return cntUpdateVenta()

@venta_bp.route('/delete', methods=['DELETE'])
def deleteVenta():
    return cntDeleteVenta()

# http://127.0.0.1:5000/ventas/
# http://127.0.0.1:5000/ventas/create
# http://127.0.0.1:5000/ventas/edit/<id>
# http://127.0.0.1:5000/ventas/delete/<id>
