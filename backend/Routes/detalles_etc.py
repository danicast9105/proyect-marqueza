from flask import Blueprint
from Controllers.detalle_controller import cntListDetalles, cntCreateDetalle, cntUpdateDetalle, cntDeleteDetalle

detalle_bp = Blueprint('detalle_bp', __name__)

@detalle_bp.route('/', methods=['GET'])
def listDetalles():
    return cntListDetalles()

@detalle_bp.route('/create', methods=['POST'])
def createDetalle():
    return cntCreateDetalle()

@detalle_bp.route('/edit', methods=['PUT'])
def updateDetalle():
    return cntUpdateDetalle()

@detalle_bp.route('/delete', methods=['DELETE'])
def deleteDetalle():
    return cntDeleteDetalle()

# http://127.0.0.1:5000/detalles/
# http://127.0.0.1:5000/detalles/create
# http://127.0.0.1:5000/detalles/edit
# http://127.0.0.1:5000/detalles/delete