from flask import Blueprint, jsonify
from Controllers.cliente_controller import cliente_controller

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/', methods=['GET'])
def listCliente():
    x = cliente_controller.cntListCliente()
    return x

@cliente_bp.route('/', methods=['POST'])
def createCliente():
    x = cliente_controller.cntAddCliente()
    return x

@cliente_bp.route('/', methods=['PUT'])
def updateCliente():
    x = cliente_controller.cntModCliente()
    return x

@cliente_bp.route('/', methods=['DELETE'])
def deleteCliente():
    x = cliente_controller.cntDelCliente()
    return x
