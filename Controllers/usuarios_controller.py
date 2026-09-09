from flask import jsonify, request
from Services.usuarios_services import servListUsuarios, addUsuarios, deleteUsuarios, updateUsuarios

def cntListUsuarios():
    data = servListUsuarios()
    return jsonify(data), 200

def cntAddUsuarios():
    # Validar que el cuerpo de la petición exista o que no se mande vacia
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

    # Obtener campos
    nombre = data.get("nombre")
    correo = data.get("correo")
    contrasena = data.get("contrasena")
    estado = data.get("estado", "ACTIVO")     #Valor por defecto o predeterminada que está en la BD
    det_etc_id = data.get("det_etc_id")

    # Validar campos obligatorios
    if nombre is None or correo is None or contrasena is None:
        return jsonify({"error": "Los campos 'nombre', 'correo' y 'contrasena' son obligatorios"}), 400

    # Validar que sean strings no vacíos
    if not isinstance(nombre, str) or not nombre.strip():
        return jsonify({"error": "El campo 'nombre' debe ser una cadena no vacía"}), 400
    if not isinstance(correo, str) or not correo.strip():
        return jsonify({"error": "El campo 'correo' debe ser una cadena no vacía"}), 400
    if not isinstance(contrasena, str) or not contrasena.strip():
        return jsonify({"error": "El campo 'contrasena' debe ser una cadena no vacía"}), 400

    # Validar que nombre no contenga ningun numro
    if any(c.isdigit() for c in nombre):
        return jsonify({"error": "El campo 'nombre' no debe contener números"}), 400

    # Validar estado (si es que viene, debe estar como string NO VACIO)
    if estado is not None:
        if not isinstance(estado, str) or not estado.strip():
            return jsonify({"error": "El campo 'estado' debe ser una cadena no vacía"}), 400

    # Validar det_etc_id (si es que se ingresa, debe ser un numero posisitivo)
    if det_etc_id is not None:
        try:
            det_etc_id = int(det_etc_id)
            if det_etc_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'det_etc_id' debe ser un entero positivo"}), 400

    result = addUsuarios(
        nombre.strip(),
        correo.strip(),
        contrasena.strip(),
        estado.strip() if estado else "ACTIVO",
        det_etc_id
    )
    return jsonify(result), 201

def cntDelUsuarios(id):
    data = deleteUsuarios(id)
    return jsonify(data), 200

def cntModUsuarios():
    # Validar que el cuerpo de la petición exista o que no se mande vacio o en blanco
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

    id_usuario = data.get("id")
    nombre = data.get("nombre")
    correo = data.get("correo")
    contrasena = data.get("contrasena")
    estado = data.get("estado")
    det_etc_id = data.get("det_etc_id")

    # Validar que id sea obligatorio y numero entero
    if id_usuario is None:
        return jsonify({"error": "El campo 'id' es obligatorio"}), 400
    try:
        id_usuario = int(id_usuario)
        if id_usuario <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El campo 'id' debe ser un entero positivo"}), 400

    # Verificar que al menos uno de los campos esté cambiado para actualizar 
    if (nombre is None and correo is None and contrasena is None and
        estado is None and det_etc_id is None):
        return jsonify({"error": "Debes enviar al menos un campo para actualizar"}), 400

    # Validar nombre
    if nombre is not None:
        if not isinstance(nombre, str) or not nombre.strip():
            return jsonify({"error": "El campo 'nombre' debe ser una cadena no vacía"}), 400
        if any(c.isdigit() for c in nombre):
            return jsonify({"error": "El campo 'nombre' no debe contener números"}), 400

    # Validar correo 
    if correo is not None:
        if not isinstance(correo, str) or not correo.strip():
            return jsonify({"error": "El campo 'correo' debe ser una cadena no vacía"}), 400

    # Validar contrasena 
    if contrasena is not None:
        if not isinstance(contrasena, str) or not contrasena.strip():
            return jsonify({"error": "El campo 'contrasena' debe ser una cadena no vacía"}), 400

    # Validar estado 
    if estado is not None:
        if not isinstance(estado, str) or not estado.strip():
            return jsonify({"error": "El campo 'estado' debe ser una cadena no vacía"}), 400

    # Validar det_etc_id 
    if det_etc_id is not None:
        try:
            det_etc_id = int(det_etc_id)
            if det_etc_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'det_etc_id' debe ser un entero positivo"}), 400

    result = updateUsuarios(
        id_usuario,
        nombre.strip() if nombre else None,
        correo.strip() if correo else None,
        contrasena.strip() if contrasena else None,
        estado.strip() if estado else None,
        det_etc_id
    )
    return jsonify(result), 200

