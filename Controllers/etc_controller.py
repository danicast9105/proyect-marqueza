from flask import jsonify, request
from Services.etc_services import etc_services

class etc_controller:

    def cntListETC():
        data = etc_services.servListETC()
        return jsonify(data), 200

    def cntAddETC():
        data = request.get_json(silent=True)

        etc_nombre = data["etc_nombre"]
        x = etc_services.addETC(etc_nombre)
        return jsonify(x), 200

    def cntDelETC(id):
        data = etc_services.deleteETC(id)
        return jsonify(data), 200

    def cntModETC(id):
        data = request.get_json(silent=True)

        etc_nombre = data["etc_nombre"]
        x = etc_services.updateETC(id, etc_nombre)
        return jsonify(x), 200

