from flask import Blueprint
from Controllers.ventas_controller import cntListVentas, cntAddVentas, cntDelVentas, cntModVentas, cntGetVentas

ventas_bp = Blueprint('ventas_bp', __name__)

@ventas_bp.route('/', methods=['GET'])
def listVentas():
    x = cntListVentas()
    return x

@ventas_bp.route('/<int:id>', methods=['GET'])
def getVentas(id):
    return cntGetVentas(id)

@ventas_bp.route('/', methods=['POST'])
def createVentas():
    x = cntAddVentas()
    return x

@ventas_bp.route('/<int:id>', methods=['PUT'])
def updateVentas(id):
    x = cntModVentas(id)
    return x

@ventas_bp.route('/<int:id>', methods=['DELETE'])
def deleteVentas(id):
    x = cntDelVentas(id)
    return x