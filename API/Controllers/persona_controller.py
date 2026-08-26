from flask import jsonify, request
from Services.persona_services import servListPersona, addPersona, deletePersona, updatePersona

def cntListPersona():
    data = servListPersona()
    return jsonify(data), 200

def cntAddPersona():
    data = addPersona()
    return jsonify(data), 200

def cntDelPersona():
    data = deletePersona()
    return jsonify(data), 200

def cntModPersona():
    data = updatePersona()
    return jsonify(data), 201

