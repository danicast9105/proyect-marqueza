from flask import jsonify, request
from Services.insumos_services import insumos_services

class insumos_controller:

    def cntListInsumos():
        data = insumos_services.servListInsumos()
        return jsonify(data), 200

    def cntAddInsumos():

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400
        
        codigo = data.get("codigo")
        nombre = data.get("nombre")
        cantidad = data.get("cantidad")
        precio = data.get("precio")
        estado = data.get("estado")
        usuario_id = data.get("usuario_id")
        proveedor_id = data.get("proveedor_id")
        etc_id = data.get("etc_id")

        # Validar campos obligatorios
        if (codigo is None or nombre is None or cantidad is None or
            precio is None or estado is None or usuario_id is None or
            proveedor_id is None or etc_id is None):
            return jsonify({
                "error": "Los campos 'codigo', 'nombre', 'cantidad', 'precio', 'estado', 'usuario_id', 'proveedor_id' y 'etc_id' son obligatorios"
            }), 400

        # Validar codigo 
        if not isinstance(codigo, str) or not codigo.strip():
            return jsonify({"error": "El campo 'codigo' debe ser una cadena no vacía"}), 400
        codigo = codigo.strip()

        # Validar nombre
        if not isinstance(nombre, str) or not nombre.strip():
            return jsonify({"error": "El campo 'nombre' debe ser una cadena no vacía"}), 400
        if any(c.isdigit() for c in nombre):
            return jsonify({"error": "El campo 'nombre' no debe contener números"}), 400
        nombre = nombre.strip()

        # Validar cantidad
        try:
            cantidad = int(cantidad)
            if cantidad < 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'cantidad' debe ser un entero mayor o igual a 0"}), 400

        # Validar precio
        try:
            precio = int(precio)
            if precio <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'precio' debe ser un entero positivo"}), 400

        # Validar estado
        if not isinstance(estado, str) or not estado.strip():
            return jsonify({"error": "El campo 'estado' debe ser una cadena no vacía"}), 400
        estado = estado.strip()

        # Validar usuario_id
        try:
            usuario_id = int(usuario_id)
            if usuario_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'usuario_id' debe ser un entero positivo"}), 400

        # Validar proveedor_id
        try:
            proveedor_id = int(proveedor_id)
            if proveedor_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'proveedor_id' debe ser un entero positivo"}), 400

        # Validar etc_id
        try:
            etc_id = int(etc_id)
            if etc_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'etc_id' debe ser un entero positivo"}), 400

        x = insumos_services.addInsumos(
            codigo, nombre, cantidad, precio, estado,
            usuario_id, proveedor_id, etc_id
        )
        return jsonify(x), 200


    def cntDelInsumos(id):
        data = insumos_services.deleteInsumos(id)
        return jsonify(data), 200


    def cntModInsumos(id):
        try:
            id = int(id)
            if id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El ID debe ser un entero positivo"}), 400

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        codigo = data.get("codigo")
        nombre = data.get("nombre")
        cantidad = data.get("cantidad")
        precio = data.get("precio")
        estado = data.get("estado")
        usuario_id = data.get("usuario_id")
        proveedor_id = data.get("proveedor_id")
        etc_id = data.get("etc_id")

        # Verificar que al menos un campo llegue para actualizar
        if (codigo is None and nombre is None and cantidad is None and
            precio is None and estado is None and usuario_id is None and
            proveedor_id is None and etc_id is None):
            return jsonify({"error": "Debes enviar al menos un campo para actualizar"}), 400

        # Validar codigo 
        if codigo is not None:
            if not isinstance(codigo, str) or not codigo.strip():
                return jsonify({"error": "El campo 'codigo' debe ser una cadena no vacía"}), 400
            codigo = codigo.strip()

        # Validar nombre 
        if nombre is not None:
            if not isinstance(nombre, str) or not nombre.strip():
                return jsonify({"error": "El campo 'nombre' debe ser una cadena no vacía"}), 400
            if any(c.isdigit() for c in nombre):
                return jsonify({"error": "El campo 'nombre' no debe contener números"}), 400
            nombre = nombre.strip()

        # Validar cantidad 
        if cantidad is not None:
            try:
                cantidad = int(cantidad)
                if cantidad < 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'cantidad' debe ser un entero mayor o igual a 0"}), 400

        # Validar precio 
        if precio is not None:
            try:
                precio = int(precio)
                if precio <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'precio' debe ser un entero positivo"}), 400

        # Validar estado 
        if estado is not None:
            if not isinstance(estado, str) or not estado.strip():
                return jsonify({"error": "El campo 'estado' debe ser una cadena no vacía"}), 400
            estado = estado.strip()

        # Validar usuario_id 
        if usuario_id is not None:
            try:
                usuario_id = int(usuario_id)
                if usuario_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'usuario_id' debe ser un entero positivo"}), 400

        # Validar proveedor_id 
        if proveedor_id is not None:
            try:
                proveedor_id = int(proveedor_id)
                if proveedor_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'proveedor_id' debe ser un entero positivo"}), 400

        # Validar etc_id 
        if etc_id is not None:
            try:
                etc_id = int(etc_id)
                if etc_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'etc_id' debe ser un entero positivo"}), 400


        x = insumos_services.updateInsumos(
            id, codigo, nombre, cantidad, precio, estado,
            usuario_id, proveedor_id, etc_id
        )
        return jsonify(x), 201
