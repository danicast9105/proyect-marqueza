from flask import Blueprint, jsonify
from Controllers.ventas_controller import cntListVentas, cntAddVentas, cntDelVentas, cntModVentas

ventas_bp = Blueprint('ventas_bp', __name__)

@ventas_bp.route('/', methods=['GET'])
def listVentas():
    x = cntListVentas()
    return x

@ventas_bp.route('/', methods=['POST'])
def createVentas():
    x = cntAddVentas
    return x

@ventas_bp.route('/', methods=['PUT'])
def updateVentas():
    x = cntModVentas
    return x

@ventas_bp.route('/', methods=['DELETE'])
def deleteVentas():
    x = cntDelVentas
    return x