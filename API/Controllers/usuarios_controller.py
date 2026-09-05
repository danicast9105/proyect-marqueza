from flask import jsonify, request
from Services.usuarios_services import servListUsuarios, addUsuarios, deleteUsuarios, updateUsuarios

def cntListUsuarios():
    data = servListUsuarios()
    return jsonify(data), 200

def cntAddUsuarios():
    data = addUsuarios()
    return jsonify(data), 200

def cntDelUsuarios():
    data = deleteUsuarios()
    return jsonify(data), 200

def cntModUsuarios():
    data = updateUsuarios()
    return jsonify(data), 201

