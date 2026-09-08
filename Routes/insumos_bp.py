from flask import Blueprint, jsonify
from Controllers.insumos_controller import insumos_controller
insumos_bp = Blueprint('insumos_bp', __name__)

@insumos_bp.route('/', methods=['GET'])
def listInsumos():
    x = insumos_controller.cntListInsumos()
    return x

@insumos_bp.route('/', methods=['POST'])
def createInsumos():
    x = insumos_controller.cntAddInsumos()
    return x

@insumos_bp.route('/<id>', methods=['PUT'])
def updateInsumos(id):
    x = insumos_controller.cntModInsumos(id)
    return x

@insumos_bp.route('/<id>', methods=['DELETE'])
def deleteInsumos(id):
    x = insumos_controller.cntDelInsumos(id)
    return x