from flask import Blueprint, jsonify
from Controllers.ventas_controller import ventas_controller

ventas_bp = Blueprint('ventas_bp', __name__)

@ventas_bp.route('/', methods=['GET'])
def listVentas():
    x = ventas_controller.cntListVentas()
    return x

@ventas_bp.route('/', methods=['POST'])
def createVentas():
    x = ventas_controller.cntAddVentas()
    return x

@ventas_bp.route('/<id>', methods=['PUT'])
def updateVentas(id):
    x = ventas_controller.cntModVentas(id)
    return x

@ventas_bp.route('/<id>', methods=['DELETE'])
def deleteVentas(id):
    x = ventas_controller.cntDelVentas(id)
    return x
