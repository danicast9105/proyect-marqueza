from flask import jsonify, request
from Services.produ_insum_services import servListProduInsum, addProduInsum, deleteProduInsum, updateProduInsum

def cntListProduInsum():
    data = servListProduInsum()
    return jsonify(data), 200

def cntAddProduInsum():
    data = addProduInsum()
    return jsonify(data), 200

def cntDelProduInsum():
    data = deleteProduInsum()
    return jsonify(data), 200

def cntModProduInsum():
    data = updateProduInsum()
    return jsonify(data), 201

