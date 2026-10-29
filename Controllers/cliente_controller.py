from flask import jsonify, request
from Services.cliente_services import cliente_services
from Controllers.request_validation import obtener_campos_faltantes

class cliente_controller:
    def cntListCliente():
        data = cliente_services.servListCliente()
        return jsonify(data), 200

    def cntGetCliente(id):
        data = cliente_services.getCliente(id)
        if data is None:
            return jsonify({"error": "Cliente no encontrado"}), 404
        return jsonify(data), 200

    def cntAddCliente():
        # Validar que el cuerpo del json no esté vacio 
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "El cuerpo debe ser un objeto JSON"}), 400

        campos_requeridos = ("persona_id",)
        campos_faltantes = obtener_campos_faltantes(data, campos_requeridos)
        if campos_faltantes:
            return jsonify({
                "error": "Faltan campos obligatorios",
                "campos_faltantes": campos_faltantes
            }), 400

        persona_id = data["persona_id"]

        # Validar que el id de persona sea num positivo
        try:
            persona_id = int(persona_id)
            if persona_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'persona_id' debe ser un entero positivo"}), 400

     
        result = cliente_services.addCliente(persona_id)
        return jsonify(result), 200

    def cntDelCliente(id):
        data = cliente_services.deleteCliente(id)
        return jsonify(data), 200

    def cntModCliente(id):
        
        try:
            id = int(id)
            if id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El ID debe ser un entero positivo"}), 400

        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "El cuerpo debe ser un objeto JSON"}), 400

        campos_faltantes = obtener_campos_faltantes(data, ("persona_id",))
        if campos_faltantes:
            return jsonify({
                "error": "Faltan campos obligatorios",
                "campos_faltantes": campos_faltantes
            }), 400

        persona_id = data["persona_id"]

        # ID persona debe ser numero positivo 
        try:
            persona_id = int(persona_id)
            if persona_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'persona_id' debe ser un entero positivo"}), 400

        result = cliente_services.updateCliente(id, persona_id)
        return jsonify(result), 200
