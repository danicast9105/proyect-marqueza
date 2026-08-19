from flask import Blueprint
from Controllers.proveedor_controller import cntListProveedores, cntCreateProveedor, cntUpdateProveedor, cntDeleteProveedor

proveedor_bp = Blueprint('proveedor_bp', __name__)

@proveedor_bp.route('/', methods=['GET'])
def listProveedores():
    return cntListProveedores()

@proveedor_bp.route('/create', methods=['POST'])
def createProveedor():
    return cntCreateProveedor()

@proveedor_bp.route('/edit/<int:id>', methods=['PUT'])
def updateProveedor():
    return cntUpdateProveedor()

@proveedor_bp.route('/delete/<int:id>', methods=['DELETE'])
def deleteProveedor():
    return cntDeleteProveedor()

# http://127.0.0.1:5000/proveedores/
# http://127.0.0.1:5000/proveedores/create
# http://127.0.0.1:5000/proveedores/edit/<id>
# http://127.0.0.1:5000/proveedores/delete/<id>
