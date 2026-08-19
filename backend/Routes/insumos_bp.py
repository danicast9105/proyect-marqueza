from flask import Blueprint
from Controllers.insumo_controller import cntListInsumos, cntCreateInsumo, cntUpdateInsumo, cntDeleteInsumo

insumo_bp = Blueprint('insumo_bp', __name__)

@insumo_bp.route('/', methods=['GET'])
def listInsumos():
    return cntListInsumos()

@insumo_bp.route('/create', methods=['POST'])
def createInsumo():
    return cntCreateInsumo()

@insumo_bp.route('/edit', methods=['PUT'])
def updateInsumo(id):
    return cntUpdateInsumo(id)

@insumo_bp.route('/delete', methods=['DELETE'])
def deleteInsumo(id):
    return cntDeleteInsumo(id)

# http://127.0.0.1:5000/insumos/
# http://127.0.0.1:5000/insumos/create
# http://127.0.0.1:5000/insumos/edit/<id>
# http://127.0.0.1:5000/insumos/delete/<id>
