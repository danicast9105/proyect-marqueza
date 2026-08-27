from flask import jsonify, request
from Services.persona_services import persona_services

class persona_controller:
    def cntListPersona():
        data = persona_services.servListPersona()
        return jsonify(data), 200

    def cntAddPersona():
        data = request.get_json(silent=True)

        nombre = data["nombre"]
        seg_nombre = data["seg_nombre"]
        pri_apellido = data["pri_apellido"]
        seg_apellido = data["seg_apellido"]
        correo = data["correo"]
        identificacion = data["identificacion"]
        telefono = data["telefono"]

        x = persona_services.addPersona(nombre, seg_nombre, pri_apellido, seg_apellido, correo, identificacion, telefono)
        return jsonify(x), 200

    def cntDelPersona(id):
        data = persona_services.deletePersona(id)
        return jsonify(data), 200

    def cntModPersona(id):
        data = request.get_json(silent=True)

        nombre = data["nombre"]
        seg_nombre = data["seg_nombre"]
        pri_apellido = data["pri_apellido"]
        seg_apellido = data["seg_apellido"]
        correo = data["correo"]
        identificacion = data["identificacion"]
        telefono = data["telefono"]

        x = persona_services.updatePersona(id, nombre, seg_nombre, pri_apellido, seg_apellido, correo, identificacion, telefono)
        return jsonify(x), 200

