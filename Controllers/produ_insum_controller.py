from flask import jsonify, request
from Services.produ_insum_services import produ_insum_services

class produ_insum_controller:

    def cntListProduInsum():
        data = produ_insum_services.servListProduInsum()
        return jsonify(data), 200

    def cntAddProduInsum():

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        cantidad = data.get("cantidad")
        producto_id = data.get("producto_id")
        insumo_id = data.get("insumo_id")

        # Validar campos
        if cantidad is None or producto_id is None or insumo_id is None:
            return jsonify({
                "error": "Los campos 'cantidad', 'producto_id' e 'insumo_id' son obligatorios"
            }), 400

        # Validar cantidad
        try:
            cantidad = int(cantidad)
            if cantidad < 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'cantidad' debe ser un entero mayor o igual a 0"}), 400

        # Validar producto_id
        try:
            producto_id = int(producto_id)
            if producto_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'producto_id' debe ser un entero positivo"}), 400

        # Validar insumo_id
        try:
            insumo_id = int(insumo_id)
            if insumo_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'insumo_id' debe ser un entero positivo"}), 400

        x = produ_insum_services.addProduInsum(cantidad, producto_id, insumo_id)
        return jsonify(x), 200

    def cntDelProduInsum(id):
        data = produ_insum_services.deleteProduInsum(id)
        return jsonify(data), 200

    def cntModProduInsum(id):
        try:
            id = int(id)
            if id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El ID debe ser un entero positivo"}), 400

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        # Obtener campos 
        cantidad = data.get("cantidad")
        producto_id = data.get("producto_id")
        insumo_id = data.get("insumo_id")

        # Verificar que al menos un campo llegue para actualizar
        if cantidad is None and producto_id is None and insumo_id is None:
            return jsonify({"error": "Debes enviar al menos un campo para actualizar"}), 400

        # Validar cantidad
        if cantidad is not None:
            try:
                cantidad = int(cantidad)
                if cantidad < 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'cantidad' debe ser un entero mayor o igual a 0"}), 400

        # Validar producto_id 
        if producto_id is not None:
            try:
                producto_id = int(producto_id)
                if producto_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'producto_id' debe ser un entero positivo"}), 400

        # Validar insumo_id 
        if insumo_id is not None:
            try:
                insumo_id = int(insumo_id)
                if insumo_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'insumo_id' debe ser un entero positivo"}), 400

        x = produ_insum_services.updateProduInsum(id, cantidad, producto_id, insumo_id)
        return jsonify(x), 200
