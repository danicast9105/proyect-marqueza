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

@contacto_bp.route('/<id>', methods=['PUT'])
def updatecontacto(id):
    x = contacto_controller.cntModContacto(id)
    return x

@contacto_bp.route('/<id>', methods=['DELETE'])
def deletecontacto(id):
    x = contacto_controller.cntDelContacto(id)
    return x