from flask import Blueprint, jsonify
from Controllers.produ_insum_controller import produ_insum_controller
produ_insum_bp = Blueprint('produ_insum_bp', __name__)

@produ_insum_bp.route('/', methods=['GET'])
def listProduInsum():
    x = produ_insum_controller.cntListProduInsum()
    return x

@produ_insum_bp.route('/', methods=['POST'])
def createProduInsum():
    x = produ_insum_controller.cntAddProduInsum()
    return x

@produ_insum_bp.route('/<id>', methods=['PUT'])
def updateProduInsum(id):
    x = produ_insum_controller.cntModProduInsum(id)
    return x

@produ_insum_bp.route('/<id>', methods=['DELETE'])
def deleteProduInsum(id):
    x = produ_insum_controller.cntDelProduInsum(id)
    return x