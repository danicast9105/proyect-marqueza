from flask import jsonify, request
from Services.contacto_services import servListContacto, servAddContacto, servDelContacto, servModContacto

def cntListContacto():
    data = servListContacto()
    return jsonify(data), 200

def cntAddContacto():
    data = servAddContacto()
    return jsonify(data), 200

def cntDelContacto():
    data = servDelContacto()
    return jsonify(data), 200

def cntModContacto():
    data = servModContacto()
    return jsonify(data), 201

