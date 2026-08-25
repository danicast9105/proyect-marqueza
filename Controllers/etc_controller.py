from flask import jsonify, request
from Services.etc_services import servListETC, addETC, deleteETC, updateETC

def cntListETC():
    data = servListETC()
    return jsonify(data), 200

def cntAddETC():
    data = addETC()
    return jsonify(data), 200

def cntDelETC():
    data = deleteETC()
    return jsonify(data), 200

def cntModETC():
    data = updateETC()
    return jsonify(data), 201

