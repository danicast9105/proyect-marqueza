from flask import Blueprint
from Controllers.cliente_controller import cntListClientes, cntCreateCliente, cntUpdateCliente, cntDeleteCliente

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/', methods=['GET'])
def listClientes():
    return cntListClientes()

@cliente_bp.route('/create', methods=['POST'])
def createCliente():
    return cntCreateCliente()

@cliente_bp.route('/edit/<int:id>', methods=['PUT'])
def updateCliente(id):
    return cntUpdateCliente(id)

@cliente_bp.route('/delete/<int:id>', methods=['DELETE'])
def deleteCliente(id):
    return cntDeleteCliente(id)

# http://127.0.0.1:5000/clientes/
# http://127.0.0.1:5000/clientes/create
# http://127.0.0.1:5000/clientes/edit/<id>
# http://127.0.0.1:5000/clientes/delete/<id>
