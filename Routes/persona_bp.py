from flask import Blueprint, jsonify
from Controllers.persona_controller import persona_controller

persona_bp = Blueprint('persona_bp', __name__)

@persona_bp.route('/', methods=['GET'])
def listPersona():
    x = persona_controller.cntListPersona()
    return x

@persona_bp.route('/', methods=['POST'])
def createPersona():
    x = persona_controller.cntAddPersona()
    return x

@persona_bp.route('/<id>', methods=['PUT'])
def updatePersona(id):
    x = persona_controller.cntModPersona(id)
    return x

@persona_bp.route('/<id>', methods=['DELETE'])
def deletePersona(id):
    x = persona_controller.cntDelPersona(id)
    return x