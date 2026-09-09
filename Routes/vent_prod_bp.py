from flask import Blueprint, jsonify
from Controllers.vent_prod_controller import cntListVentProd, cntAddVentProd, cntDelVentProd, cntModVentProd

vent_prod_bp = Blueprint('vent_prod_bp', __name__)

@vent_prod_bp.route('/', methods=['GET'])
def listVentProd():
    x = cntListVentProd()
    return x

@vent_prod_bp.route('/', methods=['POST'])
def createVentProd():
    x = cntAddVentProd
    return x

@vent_prod_bp.route('/', methods=['PUT'])
def updateVentProd():
    x = cntModVentProd
    return x

@vent_prod_bp.route('/', methods=['DELETE'])
def deleteVentProd():
    x = cntDelVentProd
    return x