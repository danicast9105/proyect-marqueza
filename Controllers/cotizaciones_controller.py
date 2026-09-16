from flask import jsonify, request
from Services.cotizaciones_services import cotizaciones_services

class cotizaciones_controller:

    def cntListCotizaciones():
        data = cotizaciones_services.servListCotizaciones()
        return jsonify(data), 200

    def cntGetCotizaciones(id):
        data = cotizaciones_services.getCotizaciones(id)
        if data is None:
            return jsonify({"error": "Cotización no encontrada"}), 404
        return jsonify(data), 200

    def cntAddCotizaciones():
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        pro_codigo = data.get("pro_codigo")
        pro_nombre = data.get("pro_nombre")
        pro_cantidad = data.get("pro_cantidad")
        pro_precio = data.get("pro_precio")
        total_pagar = data.get("total_pagar")
        usuario_id = data.get("usuario_id")
        cliente_id = data.get("cliente_id")

        if (pro_codigo is None or pro_nombre is None or pro_cantidad is None or
            pro_precio is None or total_pagar is None or usuario_id is None or
            cliente_id is None):
            return jsonify({
                "error": "Los campos 'pro_codigo', 'pro_nombre', 'pro_cantidad', 'pro_precio', 'total_pagar', 'usuario_id' y 'cliente_id' son obligatorios"
            }), 400

        if not isinstance(pro_codigo, str) or not pro_codigo.strip():
            return jsonify({"error": "El campo 'pro_codigo' debe ser una cadena no vacía"}), 400
        pro_codigo = pro_codigo.strip()


        if not isinstance(pro_nombre, str) or not pro_nombre.strip():
            return jsonify({"error": "El campo 'pro_nombre' debe ser una cadena no vacía"}), 400
        if any(c.isdigit() for c in pro_nombre):
            return jsonify({"error": "El campo 'pro_nombre' no debe contener números"}), 400
        pro_nombre = pro_nombre.strip()

        try:
            pro_cantidad = int(pro_cantidad)
            if pro_cantidad <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'pro_cantidad' debe ser un entero positivo"}), 400

        #Campo precio debe ser num positivo
        try:
            pro_precio = int(pro_precio)
            if pro_precio <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'pro_precio' debe ser un entero positivo"}), 400

        #Campo total a pagar debe ser num positivo
        try:
            total_pagar = int(total_pagar)
            if total_pagar <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'total_pagar' debe ser un entero positivo"}), 400

        #Usuario id debe ser num positivo
        try:
            usuario_id = int(usuario_id)
            if usuario_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'usuario_id' debe ser un entero positivo"}), 400

        # cliente id num positivo
        try:
            cliente_id = int(cliente_id)
            if cliente_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'cliente_id' debe ser un entero positivo"}), 400

        x = cotizaciones_services.addCotizaciones(
            pro_codigo,
            pro_nombre,
            pro_cantidad,
            pro_precio,
            total_pagar,
            usuario_id,
            cliente_id
        )
        return jsonify(x), 200

    def cntDelCotizaciones(id):
        try:
            id = int(id)
            if id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El ID debe ser un entero positivo"}), 400

        data = cotizaciones_services.deleteCotizaciones(id)

        if not data:
            return jsonify({"error": "Cotización no encontrada"}), 404

        return jsonify(data), 200

    def cntModCotizaciones(id):
        try:
            id = int(id)
            if id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "El ID debe ser un entero positivo"}), 400

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "El cuerpo de la petición es obligatorio"}), 400

        pro_codigo = data.get("pro_codigo")
        pro_nombre = data.get("pro_nombre")
        pro_cantidad = data.get("pro_cantidad")
        pro_precio = data.get("pro_precio")
        total_pagar = data.get("total_pagar")
        usuario_id = data.get("usuario_id")
        cliente_id = data.get("cliente_id")

        if (pro_codigo is None and pro_nombre is None and pro_cantidad is None and
            pro_precio is None and total_pagar is None and usuario_id is None and
            cliente_id is None):
            return jsonify({"error": "Debes enviar al menos un campo para actualizar"}), 400

        if pro_codigo is not None:
            if not isinstance(pro_codigo, str) or not pro_codigo.strip():
                return jsonify({"error": "El campo 'pro_codigo' debe ser una cadena no vacía"}), 400
            if len(pro_codigo.strip()) > 45:
                return jsonify({"error": "El campo 'pro_codigo' no puede superar los 45 caracteres"}), 400
            pro_codigo = pro_codigo.strip()

        if pro_nombre is not None:
            if not isinstance(pro_nombre, str) or not pro_nombre.strip():
                return jsonify({"error": "El campo 'pro_nombre' debe ser una cadena no vacía"}), 400
            if any(c.isdigit() for c in pro_nombre):
                return jsonify({"error": "El campo 'pro_nombre' no debe contener números"}), 400
            if len(pro_nombre.strip()) > 45:
                return jsonify({"error": "El campo 'pro_nombre' no puede superar los 45 caracteres"}), 400
            pro_nombre = pro_nombre.strip()

        if pro_cantidad is not None:
            try:
                pro_cantidad = int(pro_cantidad)
                if pro_cantidad <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'pro_cantidad' debe ser un entero positivo"}), 400

        if pro_precio is not None:
            try:
                pro_precio = int(pro_precio)
                if pro_precio <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'pro_precio' debe ser un entero positivo"}), 400

        if total_pagar is not None:
            try:
                total_pagar = int(total_pagar)
                if total_pagar <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'total_pagar' debe ser un entero positivo"}), 400

        if usuario_id is not None:
            try:
                usuario_id = int(usuario_id)
                if usuario_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'usuario_id' debe ser un entero positivo"}), 400

        if cliente_id is not None:
            try:
                cliente_id = int(cliente_id)
                if cliente_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "El campo 'cliente_id' debe ser un entero positivo"}), 400

        x = cotizaciones_services.updateCotizaciones(
            id,
            pro_codigo,
            pro_nombre,
            pro_cantidad,
            pro_precio,
            total_pagar,
            usuario_id,
            cliente_id
        )
        return jsonify(x), 200
