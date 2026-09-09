from flask import Blueprint, jsonify
from Controllers.detalles_etc_controller import detalles_etc_controller

detalles_etc_bp = Blueprint('detalles_etc_bp', __name__)

@detalles_etc_bp.route('/', methods=['GET'])
def listDetalles_etc():
    x = detalles_etc_controller.cntListDetalles_etc()
    return x

@detalles_etc_bp.route('/', methods=['POST'])
def createDetalles_etc():
    x = detalles_etc_controller.cntAddDetalles_etc()
    return x

@detalles_etc_bp.route('/<id>', methods=['PUT'])
def updateDetalles_etc(id):
    x = detalles_etc_controller.cntModDetalles_etc(id)
    return x

@detalles_etc_bp.route('/<id>', methods=['DELETE'])
def deleteDetalles_etc(id):
    x = detalles_etc_controller.cntDelDetalles_etc(id)
    return x