from flask import jsonify, request
from Services.productos_services import (
    servListProductos,
    getProductos,
    addProductos,
    deleteProductos,
    updateProductos
)
from Controllers.request_validation import obtener_campos_faltantes


def cntListProductos():
    return jsonify(servListProductos()), 200


def cntGetProductos(id):
    data = getProductos(id)
    if data is None:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(data), 200


def cntAddProductos():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "El cuerpo debe ser un objeto JSON"}), 400

    campos_requeridos = (
        "codigo", "nombre", "cantidad", "precio", "estado",
        "usuario_id", "etc_id"
    )
    campos_faltantes = obtener_campos_faltantes(data, campos_requeridos)
    if campos_faltantes:
        return jsonify({
            "error": "Faltan campos obligatorios",
            "campos_faltantes": campos_faltantes
        }), 400

    codigo = data["codigo"]
    nombre = data["nombre"]
    cantidad = data["cantidad"]
    precio = data["precio"]
    estado = data["estado"]
    usuario_id = data["usuario_id"]
    etc_id = data["etc_id"]

    if not isinstance(codigo, str):
        return jsonify({"error": "El campo 'codigo' debe ser una cadena no vacía"}), 400
    if not isinstance(nombre, str):
        return jsonify({"error": "El campo 'nombre' debe ser una cadena no vacía"}), 400
    if any(c.isdigit() for c in nombre):
        return jsonify({"error": "El campo 'nombre' no debe contener números"}), 400
    if not isinstance(estado, str):
        return jsonify({"error": "El campo 'estado' debe ser una cadena no vacía"}), 400

    try:
        cantidad = int(cantidad)
        if cantidad < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El campo 'cantidad' debe ser un entero mayor o igual a 0"}), 400

    try:
        precio = int(precio)
        if precio <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El campo 'precio' debe ser un entero positivo"}), 400

    try:
        usuario_id = int(usuario_id)
        if usuario_id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El campo 'usuario_id' debe ser un entero positivo"}), 400

    try:
        etc_id = int(etc_id)
        if etc_id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El campo 'etc_id' debe ser un entero positivo"}), 400

    result = addProductos(
        codigo.strip(),
        nombre.strip(),
        cantidad,
        precio,
        estado.strip(),
        usuario_id,
        etc_id
    )
    return jsonify(result), 200


def cntDelProductos(id):
    return jsonify(deleteProductos(id)), 200


def cntModProductos(id):
    try:
        id = int(id)
        if id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "El ID debe ser un entero positivo"}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "El cuerpo debe ser un objeto JSON"}), 400

    campos = ("codigo", "nombre", "cantidad", "precio", "estado", "usuario_id", "etc_id")
    if all(data.get(campo) is None for campo in campos):
        return jsonify({"error": "Debes enviar al menos un campo para actualizar"}), 400

    codigo = data.get("codigo")
    nombre = data.get("nombre")
    cantidad = data.get("cantidad")
    precio = data.get("precio")
    estado = data.get("estado")
    usuario_id = data.get("usuario_id")
    etc_id = data.get("etc_id")

    if codigo is not None:
        if not isinstance(codigo, str) or not codigo.strip():
            return jsonify({"error": "El campo 'codigo' debe ser una cadena no vacía"}), 400
        codigo = codigo.strip()

    if nombre is not None:
        if not isinstance(nombre, str) or not nombre.strip():
            return jsonify({"error": "El campo 'nombre' debe ser una cadena no vacía"}), 400
        if any(c.isdigit() for c in nombre):
            return jsonify({"error": "El campo 'nombre' no debe contener números"}), 400
        nombre = nombre.strip()

    if cantidad is not None:
        try:
            cantidad = int(cantidad)
            if cantidad < 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'cantidad' debe ser un entero mayor o igual a 0"}), 400

    if precio is not None:
        try:
            precio = int(precio)
            if precio <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'precio' debe ser un entero positivo"}), 400

    if estado is not None:
        if not isinstance(estado, str) or not estado.strip():
            return jsonify({"error": "El campo 'estado' debe ser una cadena no vacía"}), 400
        estado = estado.strip()

    if usuario_id is not None:
        try:
            usuario_id = int(usuario_id)
            if usuario_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'usuario_id' debe ser un entero positivo"}), 400

    if etc_id is not None:
        try:
            etc_id = int(etc_id)
            if etc_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'etc_id' debe ser un entero positivo"}), 400

    result = updateProductos(
        id,
        codigo,
        nombre,
        cantidad,
        precio,
        estado,
        usuario_id,
        etc_id
    )
    return jsonify(result), 201
