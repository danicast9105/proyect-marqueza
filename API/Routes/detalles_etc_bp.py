from flask import Blueprint, jsonify
from Controllers.detalles_etc_controller import cntListDetalles_etc, cntAddDetalles_etc, cntDelDetalles_etc, cntModDetalles_etc

detalles_etc_bp = Blueprint('detalles_etc_bp', __name__)

@detalles_etc_bp.route('/', methods=['GET'])
def listDetalles_etc():
    x = cntListDetalles_etc()
    return x

@detalles_etc_bp.route('/', methods=['POST'])
def createDetalles_etc():
    x = cntAddDetalles_etc
    return x

@detalles_etc_bp.route('/', methods=['PUT'])
def updateDetalles_etc():
    x = cntModDetalles_etc
    return x

@detalles_etc_bp.route('/', methods=['DELETE'])
def deleteDetalles_etc():
    x = cntDelDetalles_etc
    return x