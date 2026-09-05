from flask import Blueprint, jsonify
from Controllers.usuarios_controller import cntListUsuarios, cntAddUsuarios, cntDelUsuarios, cntModUsuarios

usuarios_bp = Blueprint('usuarios_bp', __name__)

@usuarios_bp.route('/', methods=['GET'])
def listUsuarios():
    x = cntListUsuarios()
    return x

@usuarios_bp.route('/', methods=['POST'])
def createUsuarios():
    x = cntAddUsuarios
    return x

@usuarios_bp.route('/', methods=['PUT'])
def updateUsuarios():
    x = cntModUsuarios
    return x

@usuarios_bp.route('/', methods=['DELETE'])
def deleteUsuarios():
    x = cntDelUsuarios
    return x