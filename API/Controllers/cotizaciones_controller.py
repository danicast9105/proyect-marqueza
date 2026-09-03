from flask import jsonify, request
from Services.cotizaciones_services import cotizaciones_services

class cotizaciones_controller:
    def cntListCotizaciones():
        data = cotizaciones_services.servListCotizaciones()
        return jsonify(data), 200

    def cntAddCotizaciones():
        data = request.get_json(silent=True)

        pro_codigo = data["pro_codigo"]
        pro_nombre = data["pro_nombre"]
        pro_cantidad = data["pro_cantidad"]
        pro_precio = data["pro_precio"]
        total_pagar = data["total_pagar"]
        usuario_id = data["usuario_id"]
        cliente_id = data["cliente_id"]

        x = cotizaciones_services.addCotizaciones(pro_codigo, pro_nombre, pro_cantidad, pro_precio, total_pagar, usuario_id, cliente_id)
        return jsonify(x), 200

    def cntDelCotizaciones(id):
        data = cotizaciones_services.deleteCotizaciones(id)
        return jsonify(data), 200

    def cntModCotizaciones(id):
        data = request.get_json(silent=True)
        
        pro_codigo = data["pro_codigo"]
        pro_nombre = data["pro_nombre"]
        pro_cantidad = data["pro_cantidad"]
        pro_precio = data["pro_precio"]
        total_pagar = data["total_pagar"]
        usuario_id = data["usuario_id"]
        cliente_id = data["cliente_id"]

        x = cotizaciones_services.updateCotizaciones(id, pro_codigo, pro_nombre, pro_cantidad, pro_precio, total_pagar, usuario_id, cliente_id)
        return jsonify(x), 200

