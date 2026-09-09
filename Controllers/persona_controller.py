from flask import jsonify, request
from Services.persona_services import persona_services

class persona_controller:
    def cntListPersona():
        data = persona_services.servListPersona()
        return jsonify(data), 200

    def cntAddPersona():
        data = request.get_json(silent=True)

        # Validar que el json no esté vacío
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        nombre = data.get("nombre")
        seg_nombre = data.get("seg_nombre")
        pri_apellido = data.get("pri_apellido")
        seg_apellido = data.get("seg_apellido")
        correo = data.get("correo")
        direccion = data.get("direccion")
        identificacion = data.get("identificacion")
        telefono = data.get("telefono")

        
        campos_requeridos = {
            "nombre": nombre,
            "pri_apellido": pri_apellido,
            "correo": correo,
            "direccion": direccion,
            "identificacion": identificacion,
            "telefono": telefono
        }
        
        for campo, valor in campos_requeridos.items():
            if valor is None or (isinstance(valor, str) and not valor.strip()):
                return jsonify({"error": f"El campo '{campo}' es obligatorio y no puede estar vacío"}), 400

        # Función de ayuda para saber si una cadena tiene digitos
        def contiene_digitos(cadena):
            if cadena is None:
                return False
            return any(c.isdigit() for c in cadena)

        # Validar campos de texto (sin numeros)
        campos_texto = {
            "nombre": nombre,
            "seg_nombre": seg_nombre,
            "pri_apellido": pri_apellido,
            "seg_apellido": seg_apellido,
            "correo": correo,
            "direccion": direccion
        }
        for nombre_campo, valor in campos_texto.items():
            if valor is not None and contiene_digitos(valor):
                return jsonify({"error": f"El campo '{nombre_campo}' no debe contener números"}), 400

        # Validar que identificación y teléfono sean solo dígitos
        if not identificacion.isdigit():
            return jsonify({"error": "El campo 'identificacion' debe contener solo números"}), 400
        if not telefono.isdigit():
            return jsonify({"error": "El campo 'telefono' debe contener solo números"}), 400

        x = persona_services.addPersona(
            nombre, seg_nombre, pri_apellido, seg_apellido,
            correo, direccion, identificacion, telefono
        )
        return jsonify(x), 200

    def cntDelPersona(id):
        data = persona_services.deletePersona(id)
        return jsonify(data), 200

    def cntModPersona(id):
        # Validar que el ID sea un num entero
        try:
            id = int(id)
            if id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El ID debe ser un entero positivo"}), 400

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

    
        nombre = data.get("nombre")
        seg_nombre = data.get("seg_nombre")
        pri_apellido = data.get("pri_apellido")
        seg_apellido = data.get("seg_apellido")
        correo = data.get("correo")
        direccion = data.get("direccion")
        identificacion = data.get("identificacion")
        telefono = data.get("telefono")

        # Verificar que al menos un campo esté cambiado para actualizar
        if (nombre is None and seg_nombre is None and pri_apellido is None and
            seg_apellido is None and correo is None and direccion is None and
            identificacion is None and telefono is None):
            return jsonify({"error": "Debes enviar al menos un campo para actualizar"}), 400

        # Validar nombres y apellido (que no tengan numeros)
        campos_nombre = {
            "nombre": nombre,
            "seg_nombre": seg_nombre,
            "pri_apellido": pri_apellido,
            "seg_apellido": seg_apellido
        }
        for campo, valor in campos_nombre.items():
            if valor is not None:
                if not isinstance(valor, str) or not valor.strip():
                    return jsonify({"error": f"El campo '{campo}' debe ser una cadena no vacía"}), 400
                # Verificar que no tenga dígitos
                if any(c.isdigit() for c in valor):
                    return jsonify({"error": f"El campo '{campo}' no debe contener números"}), 400

        # Validar correo 
        if correo is not None:
            if not isinstance(correo, str) or not correo.strip():
                return jsonify({"error": "El campo 'correo' debe ser una cadena no vacía"}), 400

        # Validar dirección 
        if direccion is not None:
            if not isinstance(direccion, str) or not direccion.strip():
                return jsonify({"error": "El campo 'direccion' debe ser una cadena no vacía"}), 400

        # Validar identificación
        if identificacion is not None:
            if not isinstance(identificacion, str) or not identificacion.strip():
                return jsonify({"error": "El campo 'identificacion' debe ser una cadena no vacía"}), 400
            if not identificacion.isdigit():
                return jsonify({"error": "El campo 'identificacion' debe contener solo números"}), 400

        # Validar teléfono
        if telefono is not None:
            if not isinstance(telefono, str) or not telefono.strip():
                return jsonify({"error": "El campo 'telefono' debe ser una cadena no vacía"}), 400
            if not telefono.isdigit():
                return jsonify({"error": "El campo 'telefono' debe contener solo números"}), 400

        x = persona_services.updatePersona(
            id,
            nombre,
            seg_nombre,
            pri_apellido,
            seg_apellido,
            correo,
            direccion,
            identificacion,
            telefono
        )
        return jsonify(x), 200

