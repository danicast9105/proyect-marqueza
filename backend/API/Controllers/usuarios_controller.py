from flask import jsonify, request
from Services.usuarios_services import servListUsuarios, addUsuarios, deleteUsuarios, updateUsuarios

def cntListUsuarios():
    data = servListUsuarios()
    return jsonify(data), 200

def cntAddUsuarios():
    data = request.get_json(silent=True) or {}
    required = ("nombre", "correo", "contrasena", "estado", "det_etc_id")
    missing = [field for field in required if field not in data]
    if missing:
        return jsonify({"error": f"Faltan campos: {', '.join(missing)}"}), 400

    result = addUsuarios(
        data["nombre"], data["correo"], data["contrasena"],
        data["estado"], data["det_etc_id"]
    )
    return jsonify(result), 201

def cntDelUsuarios(id):
    data = deleteUsuarios(id)
    return jsonify(data), 200

def cntModUsuarios(id):
    data = request.get_json(silent=True) or {}
    required = ("nombre", "correo", "contrasena", "estado", "det_etc_id")
    missing = [field for field in required if field not in data]
    if missing:
        return jsonify({"error": f"Faltan campos: {', '.join(missing)}"}), 400

    result = updateUsuarios(
        id, data["nombre"], data["correo"], data["contrasena"],
        data["estado"], data["det_etc_id"]
    )
    return jsonify(result), 200

