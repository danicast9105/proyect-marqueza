from flask import Blueprint, jsonify
from Controllers.etc_controller import etc_controller

etc_bp = Blueprint('etc_bp', __name__)

@etc_bp.route('/', methods=['GET'])
def listETC():
    x = etc_controller.cntListETC()
    return x

@etc_bp.route('/', methods=['POST'])
def createETC():
    x = etc_controller.cntAddETC()
    return x

@etc_bp.route('/<id>', methods=['PUT'])
def updateETC(id):
    x = etc_controller.cntModETC(id)
    return x

@etc_bp.route('/<id>', methods=['DELETE'])
def deleteETC(id):
    x = etc_controller.cntDelETC(id)
    return x