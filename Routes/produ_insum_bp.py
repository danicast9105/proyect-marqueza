from flask import Blueprint, jsonify
from Controllers.produ_insum_controller import cntListProduInsum, cntAddProduInsum, cntDelProduInsum, cntModProduInsum
produ_insum_bp = Blueprint('produ_insum_bp', __name__)

@produ_insum_bp.route('/', methods=['GET'])
def listProduInsum():
    x = cntListProduInsum()
    return x

@produ_insum_bp.route('/', methods=['POST'])
def createProduInsum():
    x = cntAddProduInsum
    return x

@produ_insum_bp.route('/', methods=['PUT'])
def updateProduInsum():
    x = cntModProduInsum
    return x

@produ_insum_bp.route('/', methods=['DELETE'])
def deleteProduInsum():
    x = cntDelProduInsum
    return x