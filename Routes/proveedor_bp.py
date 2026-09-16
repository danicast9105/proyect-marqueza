from flask import Blueprint
from Controllers.proveedor_controller import cntListProveedor, cntAddProveedor, cntDelProveedor, cntModProveedor, cntGetProveedor

proveedor_bp = Blueprint('proveedor_bp', __name__)

@proveedor_bp.route('/', methods=['GET'])
def listProveedor():
    x = cntListProveedor()
    return x

@proveedor_bp.route('/<int:id>', methods=['GET'])
def getProveedor(id):
    return cntGetProveedor(id)

@proveedor_bp.route('/', methods=['POST'])
def createProveedor():
    x = cntAddProveedor()
    return x

@proveedor_bp.route('/<int:id>', methods=['PUT'])
def updateProveedor(id):
    x = cntModProveedor(id)
    return x

@proveedor_bp.route('/<int:id>', methods=['DELETE'])
def deleteProveedor(id):
    x = cntDelProveedor(id)
    return x