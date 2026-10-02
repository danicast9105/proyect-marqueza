from flask import Blueprint, jsonify
from Controllers.vent_prod_controller import vent_prod_controller

vent_prod_bp = Blueprint('vent_prod_bp', __name__)

@vent_prod_bp.route('/', methods=['GET'])
def listVentProd():
    x = vent_prod_controller.cntListVentProd()
    return x

@vent_prod_bp.route('/', methods=['POST'])
def createVentProd():
    x = vent_prod_controller.cntAddVentProd()
    return x

@vent_prod_bp.route('/<id>', methods=['PUT'])
def updateVentProd(id):
    x = vent_prod_controller.cntModVentProd(id)
    return x

@vent_prod_bp.route('/<id>', methods=['DELETE'])
def deleteVentProd(id):
    x = vent_prod_controller.cntDelVentProd(id)
    return x
