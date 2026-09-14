from flask import jsonify, request
from Services.produ_insum_services import produ_insum_services

class produ_insum_controller:
    def cntListProduInsum():
        data = produ_insum_services.servListProduInsum()
        return jsonify(data), 200

    def cntGetProduInsum(id):
        data = produ_insum_services.getProduInsum(id)
        if data is None:
            return jsonify({"error": "Relación producto-insumo no encontrada"}), 404
        return jsonify(data), 200

    def cntAddProduInsum():
        data =  request.get_json(silent=True)

        cantidad =  data["cantidad"]
        producto_id = data["producto_id"]
        insumo_id = data["insumo_id"]
        x = produ_insum_services.addProduInsum(cantidad, producto_id, insumo_id)
        return jsonify(x), 200

    def cntDelProduInsum(id):
        data = produ_insum_services.deleteProduInsum(id)
        return jsonify(data), 200

    def cntModProduInsum(id):
        data =  request.get_json(silent=True)

        cantidad =  data["cantidad"]
        producto_id = data["producto_id"]
        insumo_id = data["insumo_id"]
        x = produ_insum_services.updateProduInsum(id, cantidad, producto_id, insumo_id)
        return jsonify(x), 200

