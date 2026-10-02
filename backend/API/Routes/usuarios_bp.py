from flask import Blueprint, jsonify
from Controllers.usuarios_controller import usuarios_controller

usuarios_bp = Blueprint('usuarios_bp', __name__)

@usuarios_bp.route('/', methods=['GET'])
def listUsuarios():
    x = usuarios_controller.cntListUsuarios()
    return x

@usuarios_bp.route('/', methods=['POST'])
def createUsuarios():
    x = usuarios_controller.cntAddUsuarios()
    return x

@usuarios_bp.route('/<id>', methods=['PUT'])
def updateUsuarios(id):
    x = usuarios_controller.cntModUsuarios(id)
    return x

@usuarios_bp.route('/<id>', methods=['DELETE'])
def deleteUsuarios(id):
    x = usuarios_controller.cntDelUsuarios(id)
    return x
