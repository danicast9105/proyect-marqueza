from flask import Blueprint, jsonify
from Controllers.etc_controller import cntListETC, cntAddETC, cntDelETC, cntModETC

etc_bp = Blueprint('etc_bp', __name__)

@etc_bp.route('/', methods=['GET'])
def listETC():
    x = cntListETC()
    return x

@etc_bp.route('/', methods=['POST'])
def createETC():
    x = cntAddETC
    return x

@etc_bp.route('/', methods=['PUT'])
def updateETC():
    x = cntModETC
    return x

@etc_bp.route('/', methods=['DELETE'])
def deleteETC():
    x = cntDelETC
    return x