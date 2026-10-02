from flask import Blueprint, jsonify
from Controllers.proveedor_controller import proveedor_controller

proveedor_bp = Blueprint('proveedor_bp', __name__)

@proveedor_bp.route('/', methods=['GET'])
def listProveedor():
    x = proveedor_controller.cntListProveedor()
    return x

@proveedor_bp.route('/', methods=['POST'])
def createProveedor():
    x = proveedor_controller.cntAddProveedor()
    return x

@proveedor_bp.route('/<id>', methods=['PUT'])
def updateProveedor(id):
    x = proveedor_controller.cntModProveedor(id)
    return x

@proveedor_bp.route('/<id>', methods=['DELETE'])
def deleteProveedor(id):
    x = proveedor_controller.cntDelProveedor(id)
    return x
