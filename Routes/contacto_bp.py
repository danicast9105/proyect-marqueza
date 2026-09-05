from flask import Blueprint, jsonify
from Controllers.contacto_controller import contacto_controller

contacto_bp = Blueprint('contacto_bp', __name__)

@contacto_bp.route('/', methods=['GET'])
def listcontacto():
    x = contacto_controller.cntListContacto()
    return x

@contacto_bp.route('/', methods=['POST'])
def createcontacto():
    x = contacto_controller.cntAddContacto()
    return x

@contacto_bp.route('/', methods=['PUT'])
def updatecontacto():
    x = contacto_controller.cntModContacto()
    return x

@contacto_bp.route('/', methods=['DELETE'])
def deletecontacto():
    x = contacto_controller.cntDelContacto()
    return x