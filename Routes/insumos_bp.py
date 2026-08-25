from flask import Blueprint, jsonify
from Controllers.insumos_controller import cntListInsumos, cntAddInsumos, cntDelInsumos, cntModInsumos

insumos_bp = Blueprint('insumos_bp', __name__)

@insumos_bp.route('/', methods=['GET'])
def listInsumos():
    x = cntListInsumos()
    return x

@insumos_bp.route('/', methods=['POST'])
def createInsumos():
    x = cntAddInsumos
    return x

@insumos_bp.route('/', methods=['PUT'])
def updateInsumos():
    x = cntModInsumos
    return x

@insumos_bp.route('/', methods=['DELETE'])
def deleteInsumos():
    x = cntDelInsumos
    return x