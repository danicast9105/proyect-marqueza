from flask import Blueprint
from Controllers.documentacion_controller import documentacion_controller

documentacion_bp = Blueprint('documentacion_bp', __name__)

@documentacion_bp.route('/', methods=['GET'])
def listDocumentacion():
    x = documentacion_controller.cntListDocumentacion()
    return x

@documentacion_bp.route('/', methods=['POST'])
def addDocumentacion():
    x = documentacion_controller.cntAddDocumentacion()
    return x

@documentacion_bp.route('/<id>', methods=['PUT'])
def updateDocumentacion(id):
    x = documentacion_controller.cntModDocumentacion(id)
    return x

@documentacion_bp.route('/<id>', methods=['DELETE'])
def deleteDocumentacion(id):
    x = documentacion_controller.cntDelDocumentacion(id)
    return x
