from flask import jsonify, request
from Services.usuarios_services import servListUsuarios, servAddUsuarios, servDelUsuarios, servModUsuarios

def cntListUsuarios():
    data = servListUsuarios()
    return jsonify(data), 200

def cntAddUsuarios():
    data = servAddUsuarios()
    return jsonify(data), 200

def cntDelUsuarios():
    data = servDelUsuarios()
    return jsonify(data), 200

def cntModUsuarios():
    data = servModUsuarios()
    return jsonify(data), 201

