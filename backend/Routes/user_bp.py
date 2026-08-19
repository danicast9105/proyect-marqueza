from flask import Blueprint, jsonify
from Controllers.user_controller import cntListUsers

us_bp = Blueprint('user_bp', __name__)

@us_bp.route('/', methods=['GET'])
def listUsers():
    x = cntListUsers()
    return x

@us_bp.route('/', methods=['POST'])
def createUser():
    return ""

@us_bp.route('/', methods=['PUT'])
def updateUser():
    return ""

@us_bp.route('/', methods=['DELETE'])
def deleteUser():
    return ""

# http://128.9.9.9/user/
# http://128.9.9.9/user/create
# http://128.9.9.9/user/edit