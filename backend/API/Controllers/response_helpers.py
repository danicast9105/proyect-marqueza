from flask import jsonify
from flask import request


def request_object():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, (jsonify({"mensaje": "El cuerpo debe ser un objeto JSON"}), 400)
    return data, None


def request_id(value):
    if isinstance(value, bool):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError, OverflowError):
        return None
    if parsed < 1 or not str(value).strip().isdigit():
        return None
    return parsed


def controller_response(result, default_status=200):
    if (
        isinstance(result, tuple)
        and len(result) == 2
        and isinstance(result[1], int)
    ):
        payload, status = result
    else:
        payload, status = result, default_status
    return jsonify(payload), status
