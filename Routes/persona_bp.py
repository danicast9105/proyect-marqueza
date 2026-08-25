from flask import Blueprint, jsonify
from Controllers.persona_controller import cntListPersona, cntAddPersona, cntDelPersona, cntModPersona

persona_bp = Blueprint('persona_bp', __name__)

@persona_bp.route('/', methods=['GET'])
def listPersona():
    x = cntListPersona()
    return x

@persona_bp.route('/', methods=['POST'])
def createPersona():
    x = cntAddPersona
    return x

@persona_bp.route('/', methods=['PUT'])
def updatePersona():
    x = cntModPersona
    return x

@persona_bp.route('/', methods=['DELETE'])
def deletePersona():
    x = cntDelPersona
    return x