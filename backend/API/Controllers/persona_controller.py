from flask import jsonify, request
from Services.persona_services import persona_services
from Controllers.response_helpers import (
    controller_response, request_id, request_object,
)

class persona_controller:
    def cntListPersona():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data = persona_services.servListPersona(id)
        return jsonify(data), 200

    def cntAddPersona():
        data, error = request_object()
        if error:
            return error

        nombre = data.get("nombre")
        seg_nombre = data.get("seg_nombre")
        pri_apellido = data.get("pri_apellido")
        seg_apellido = data.get("seg_apellido")
        correo = data.get("correo")
        direccion = data.get("direccion")
        identificacion = data.get("identificacion")
        telefono = data.get("telefono")

        x = persona_services.addPersona(nombre, seg_nombre, pri_apellido, seg_apellido, correo, direccion, identificacion, telefono)
        return controller_response(x)

    def cntDelPersona(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data = persona_services.deletePersona(id)
        return controller_response(data)

    def cntModPersona(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error

        nombre = data.get("nombre")
        seg_nombre = data.get("seg_nombre")
        pri_apellido = data.get("pri_apellido")
        seg_apellido = data.get("seg_apellido")
        correo = data.get("correo")
        direccion = data.get("direccion")
        identificacion = data.get("identificacion")
        telefono = data.get("telefono")

        x = persona_services.updatePersona(id, nombre, seg_nombre, pri_apellido, seg_apellido, correo, direccion, identificacion, telefono)
        return controller_response(x)
