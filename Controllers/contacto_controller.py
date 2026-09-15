from flask import jsonify, request
from Services.contacto_services import contacto_services

class contacto_controller:

    def cntListContacto():
        data = contacto_services.servListContacto()
        return jsonify(data), 200

    def cntAddContacto():
        # Que la peticon no esté vacia
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        tipo_contacto = data.get("tipo_contacto")
        contenido = data.get("contenido")
        proveedor_id = data.get("proveedor_id")

        # Validar campos obligatorios
        if tipo_contacto is None or contenido is None or proveedor_id is None:
            return jsonify({"error": "Los campos 'tipo_contacto', 'contenido' y 'proveedor_id' son obligatorios"}), 400

        if not isinstance(tipo_contacto, str) or not tipo_contacto.strip():
            return jsonify({"error": "El campo 'tipo_contacto' debe ser una cadena no vacía"}), 400
        if len(tipo_contacto.strip()) > 15:
            return jsonify({"error": "El campo 'tipo_contacto' no puede superar los 15 caracteres"}), 400

        if not isinstance(contenido, str) or not contenido.strip():
            return jsonify({"error": "El campo 'contenido' debe ser una cadena no vacía"}), 400

        try:
            proveedor_id = int(proveedor_id)
            if proveedor_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'proveedor_id' debe ser un entero positivo"}), 400

        result = contacto_services.addContacto(
            tipo_contacto.strip(),
            contenido.strip(),
            proveedor_id
        )
        return jsonify(result), 200

    def cntDelContacto(id):
        data = contacto_services.deleteContacto(id)
        return jsonify(data), 200

    def cntModContacto(id):
        try:
            id = int(id)
            if id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El ID debe ser un entero positivo"}), 400

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        tipo_contacto = data.get("tipo_contacto")
        contenido = data.get("contenido")
        proveedor_id = data.get("proveedor_id")

        if tipo_contacto is None and contenido is None and proveedor_id is None:
            return jsonify({"error": "Debes enviar al menos un campo para actualizar"}), 400

        if tipo_contacto is not None:
            if not isinstance(tipo_contacto, str) or not tipo_contacto.strip():
                return jsonify({"error": "El campo 'tipo_contacto' debe ser una cadena no vacía"}), 400
            
        if contenido is not None:
            if not isinstance(contenido, str) or not contenido.strip():
                return jsonify({"error": "El campo 'contenido' debe ser una cadena no vacía"}), 400
            contenido = contenido.strip()

        if proveedor_id is not None:
            try:
                proveedor_id = int(proveedor_id)
                if proveedor_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'proveedor_id' debe ser un entero positivo"}), 400

        result = contacto_services.updateContacto(
            id,
            tipo_contacto,
            contenido,
            proveedor_id
        )
        return jsonify(result), 200
