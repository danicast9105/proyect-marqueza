from flask import Blueprint
from Controllers.vent_prod_controller import cntListVentProd, cntAddVentProd, cntDelVentProd, cntModVentProd, cntGetVentProd

vent_prod_bp = Blueprint('vent_prod_bp', __name__)

@vent_prod_bp.route('/', methods=['GET'])
def listVentProd():
    x = cntListVentProd()
    return x

@vent_prod_bp.route('/<int:id>', methods=['GET'])
def getVentProd(id):
    return cntGetVentProd(id)

@vent_prod_bp.route('/', methods=['POST'])
def createVentProd():
    x = cntAddVentProd()
    return x

@vent_prod_bp.route('/<int:id>', methods=['PUT'])
def updateVentProd(id):
    x = cntModVentProd(id)
    return x

@vent_prod_bp.route('/<int:id>', methods=['DELETE'])
def deleteVentProd(id):
    x = cntDelVentProd(id)
    return x