from flask import Blueprint, jsonify
from Controllers.proveedor_controller import cntListProveedor, cntAddProveedor, cntDelProveedor, cntModProveedor

proveedor_bp = Blueprint('proveedor_bp', __name__)

@proveedor_bp.route('/', methods=['GET'])
def listProveedor():
    x = cntListProveedor()
    return x

@proveedor_bp.route('/', methods=['POST'])
def createProveedor():
    x = cntAddProveedor
    return x

@proveedor_bp.route('/', methods=['PUT'])
def updateProveedor():
    x = cntModProveedor
    return x

@proveedor_bp.route('/', methods=['DELETE'])
def deleteProveedor():
    x = cntDelProveedor
    return x