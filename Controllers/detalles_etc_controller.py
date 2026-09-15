from flask import jsonify, request
from Services.detalles_etc_services import detalles_etc_services

class detalles_etc_controller:

    def cntListDetalles_etc():
        data = detalles_etc_services.servListDetalles_etc()
        return jsonify(data), 200

    def cntAddDetalles_etc():
    
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        det_etc_nombre = data.get("det_etc_nombre")
        det_etc_etc_id = data.get("det_etc_etc_id")
        det_etc_per_id = data.get("det_etc_per_id")

        # Validar campos obligatorios
        if det_etc_nombre is None or det_etc_etc_id is None or det_etc_per_id is None:
            return jsonify({
                "error": "Los campos 'det_etc_nombre', 'det_etc_etc_id' y 'det_etc_per_id' son obligatorios"
            }), 400

        # Validar det_etc_nombre: string no vacío, sin números, máx 45
        if not isinstance(det_etc_nombre, str) or not det_etc_nombre.strip():
            return jsonify({"error": "El campo 'det_etc_nombre' debe ser una cadena no vacía"}), 400
        if any(c.isdigit() for c in det_etc_nombre):
            return jsonify({"error": "El campo 'det_etc_nombre' no debe contener números"}), 400
        det_etc_nombre = det_etc_nombre.strip()


        #El id de este campo que aun no sé que hace debe ser num positivo :)
        try:
            det_etc_etc_id = int(det_etc_etc_id)
            if det_etc_etc_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'det_etc_etc_id' debe ser un entero positivo"}), 400

        # Validar det_etc_per_id num positivo (un foraneo supongo) 
        try:
            det_etc_per_id = int(det_etc_per_id)
            if det_etc_per_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'det_etc_per_id' debe ser un entero positivo"}), 400

        x = detalles_etc_services.addDetalles_etc(
            det_etc_nombre,
            det_etc_etc_id,
            det_etc_per_id
        )
        return jsonify(x), 200

    def cntDelDetalles_etc(id):
        data = detalles_etc_services.deleteDetalles_etc(id)
        return jsonify(data), 200

    def cntModDetalles_etc(id):
       
        try:
            id = int(id)
            if id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El ID debe ser un entero positivo"}), 400

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        det_etc_nombre = data.get("det_etc_nombre")
        det_etc_etc_id = data.get("det_etc_etc_id")
        det_etc_per_id = data.get("det_etc_per_id")

        # Verificar que al menos un campo llegue para actualizar
        if det_etc_nombre is None and det_etc_etc_id is None and det_etc_per_id is None:
            return jsonify({"error": "Debes enviar al menos un campo para actualizar"}), 400

        # Validar det_etc_nombre si es que viene para actu
        if det_etc_nombre is not None:
            if not isinstance(det_etc_nombre, str) or not det_etc_nombre.strip():
                return jsonify({"error": "El campo 'det_etc_nombre' debe ser una cadena no vacía"}), 400
            if any(c.isdigit() for c in det_etc_nombre):
                return jsonify({"error": "El campo 'det_etc_nombre' no debe contener números"}), 400
            if len(det_etc_nombre.strip()) > 45:
                return jsonify({"error": "El campo 'det_etc_nombre' no puede superar los 45 caracteres"}), 400
            det_etc_nombre = det_etc_nombre.strip()

        # Validar det_etc_etc_id si viene
        if det_etc_etc_id is not None:
            try:
                det_etc_etc_id = int(det_etc_etc_id)
                if det_etc_etc_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'det_etc_etc_id' debe ser un entero positivo"}), 400

        # Validar det_etc_per_id si viene
        if det_etc_per_id is not None:
            try:
                det_etc_per_id = int(det_etc_per_id)
                if det_etc_per_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'det_etc_per_id' debe ser un entero positivo"}), 400

        x = detalles_etc_services.updateDetalles_etc(
            id,
            det_etc_nombre,
            det_etc_etc_id,
            det_etc_per_id
        )
        return jsonify(x), 200
