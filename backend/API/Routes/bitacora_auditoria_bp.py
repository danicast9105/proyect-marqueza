from flask import Blueprint, jsonify
from Controllers.bitacora_auditoria_controller import bitacora_auditoria_controller

bitacora_auditoria_bp = Blueprint('bitacora_auditoria_bp', __name__)

@bitacora_auditoria_bp.route('/', methods=['GET'])
def listBitacora():
    x = bitacora_auditoria_controller.cntListBitacora()
    return x

@bitacora_auditoria_bp.route('/', methods=['POST'])
def createBitacora():
    x = bitacora_auditoria_controller.cntAddBitacora()
    return x

@bitacora_auditoria_bp.route('/<id>', methods=['PUT'])
def updateBitacora(id):
    x = bitacora_auditoria_controller.cntModBitacora(id)
    return x

@bitacora_auditoria_bp.route('/<id>', methods=['DELETE'])
def deleteBitacora(id):
    x = bitacora_auditoria_controller.cntDelBitacora(id)
    return x
