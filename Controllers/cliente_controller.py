from flask import jsonify, request
from Services.cliente_services import cliente_services

class cliente_controller:
    def cntListCliente():
        data = cliente_services.servListCliente()
        return jsonify(data), 200

    def cntAddCliente():
        # Validar que el cuerpo del json no esté vacio 
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        persona_id = data.get("persona_id")
        if persona_id is None:
            return jsonify({"error": "El campo 'persona_id' es obligatorio"}), 400

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
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        # ID persona obligatorio
        persona_id = data.get("persona_id")
        if persona_id is None:
            return jsonify({"error": "El campo 'persona_id' es obligatorio"}), 400

        # ID persona debe ser numero positivo 
        try:
            persona_id = int(persona_id)
            if persona_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'persona_id' debe ser un entero positivo"}), 400

        result = cliente_services.updateCliente(id, persona_id)
        return jsonify(result), 200

