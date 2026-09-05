from flask import jsonify, request
from Services.detalles_etc_services import detalles_etc_services

class detalles_etc_controller:
    def cntListDetalles_etc():
        data = detalles_etc_services.servListDetalles_etc()
        return jsonify(data), 200

    def cntAddDetalles_etc():
        data = request.get_json(silent=True)

        det_etc_nombre = data["det_etc_nombre"]
        det_etc_etc_id = data["det_etc_etc_id"]
        det_etc_per_id = data["det_etc_per_id"]

        x = detalles_etc_services.addDetalles_etc(det_etc_nombre, det_etc_etc_id, det_etc_per_id)
        return jsonify(x), 200

    def cntDelDetalles_etc(id):
        data = detalles_etc_services.deleteDetalles_etc(id)
        return jsonify(data), 200

    def cntModDetalles_etc(id):
        data = request.get_json(silent=True)
        
        det_etc_nombre = data["det_etc_nombre"]
        det_etc_etc_id = data["det_etc_etc_id"]
        det_etc_per_id = data["det_etc_per_id"]

        x = detalles_etc_services.updateDetalles_etc(id, det_etc_nombre, det_etc_etc_id, det_etc_per_id)
        return jsonify(x), 200

