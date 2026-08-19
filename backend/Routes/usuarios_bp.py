from flask import Blueprint
from Controllers.usuario_controller import cntListUsuarios, cntCreateUsuario, cntUpdateUsuario, cntDeleteUsuario

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/', methods=['GET'])
def listUsuarios():
    return cntListUsuarios()

@usuario_bp.route('/create', methods=['POST'])
def createUsuario():
    return cntCreateUsuario()

@usuario_bp.route('/edit', methods=['PUT'])
def updateUsuario():
    return cntUpdateUsuario()

@usuario_bp.route('/delete', methods=['DELETE'])
def deleteUsuario():
    return cntDeleteUsuario()

# http://127.0.0.1:5000/usuarios/
# http://127.0.0.1:5000/usuarios/create
# http://127.0.0.1:5000/usuarios/edit/<id>
# http://127.0.0.1:5000/usuarios/delete/<id>
