from flask import Blueprint, jsonify
from Controllers.recuperacion_contrasena_controller import recuperacion_contrasena_controller

recuperacion_contrasena_bp = Blueprint('recuperacion_contrasena_bp', __name__)

@recuperacion_contrasena_bp.route('/', methods=['GET'])
def listRecuperacion():
    x = recuperacion_contrasena_controller.cntListRecuperacion()
    return x

@recuperacion_contrasena_bp.route('/', methods=['POST'])
def createRecuperacion():
    x = recuperacion_contrasena_controller.cntAddRecuperacion()
    return x

@recuperacion_contrasena_bp.route('/<id>', methods=['PUT'])
def updateRecuperacion(id):
    x = recuperacion_contrasena_controller.cntModRecuperacion(id)
    return x

@recuperacion_contrasena_bp.route('/<id>', methods=['DELETE'])
def deleteRecuperacion(id):
    x = recuperacion_contrasena_controller.cntDelRecuperacion(id)
    return x
