from flask import jsonify, request
from Services.etc_services import etc_services

class etc_controller:

    def cntListETC():
        data = etc_services.servListETC()
        return jsonify(data), 200

    def cntAddETC():
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        etc_nombre = data.get("etc_nombre")

        if etc_nombre is None:
            return jsonify({"error": "El campo 'etc_nombre' es obligatorio"}), 400

        # Validar tipo y contenido
        if not isinstance(etc_nombre, str) or not etc_nombre.strip():
            return jsonify({"error": "El campo 'etc_nombre' debe ser una cadena no vacía"}), 400
        if any(c.isdigit() for c in etc_nombre):
            return jsonify({"error": "El campo 'etc_nombre' no debe contener números"}), 400
        etc_nombre = etc_nombre.strip()

        x = etc_services.addETC(etc_nombre)
        return jsonify(x), 200

    def cntDelETC(id):
        # Validar que el ID sea un num positivo
        try:
            id = int(id)
            if id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El ID debe ser un entero positivo"}), 400

        data = etc_services.deleteETC(id)

        if not data:
            return jsonify({"error": "Registro ETC no encontrado"}), 404

        return jsonify(data), 200

    def cntModETC(id):

        try:
            id = int(id)
            if id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El ID debe ser un entero positivo"}), 400

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        etc_nombre = data.get("etc_nombre")

        if etc_nombre is None:
            return jsonify({"error": "El campo 'etc_nombre' es obligatorio para actualizar"}), 400

        if not isinstance(etc_nombre, str) or not etc_nombre.strip():
            return jsonify({"error": "El campo 'etc_nombre' debe ser una cadena no vacía"}), 400
        if any(c.isdigit() for c in etc_nombre):
            return jsonify({"error": "El campo 'etc_nombre' no debe contener números"}), 400
        if len(etc_nombre.strip()) > 45:
            return jsonify({"error": "El campo 'etc_nombre' no puede superar los 45 caracteres"}), 400
        etc_nombre = etc_nombre.strip()

        x = etc_services.updateETC(id, etc_nombre)
        return jsonify(x), 200
