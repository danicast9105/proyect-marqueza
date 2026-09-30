from flask import jsonify, request


def required_json(*fields):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None, (jsonify({"error": "El cuerpo debe ser un objeto JSON."}), 400)

    missing = [field for field in fields if field not in payload]
    if missing:
        return None, (jsonify({"error": "Faltan campos requeridos.", "campos": missing}), 400)

    return payload, None