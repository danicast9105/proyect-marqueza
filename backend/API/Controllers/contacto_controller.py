from flask import jsonify, request
from Services.contacto_services import contacto_services
from Controllers.response_helpers import (
    controller_response, request_id, request_object,
)

class contacto_controller:
    def cntListContacto():
        id = request.args.get("id") or None
        if id is not None:
            id = request_id(id)
            if id is None:
                return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data = contacto_services.servListContacto(id)
        return jsonify(data), 200

    def cntAddContacto():
        data, error = request_object()
        if error:
            return error

        tipo_contacto = data.get("tipo_contacto")
        contenido = data.get("contenido")
        proveedor_id = data.get("proveedor_id")

        x = contacto_services.addContacto(tipo_contacto, contenido, proveedor_id)
        return controller_response(x)

    def cntDelContacto(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data = contacto_services.deleteContacto(id)
        return controller_response(data)

    def cntModContacto(id):
        id = request_id(id)
        if id is None:
            return jsonify({"mensaje": "El ID debe ser un entero positivo"}), 400
        data, error = request_object()
        if error:
            return error

        tipo_contacto = data.get("tipo_contacto")
        contenido = data.get("contenido")
        proveedor_id = data.get("proveedor_id")

        x = contacto_services.updateContacto(id, tipo_contacto, contenido, proveedor_id)
        return controller_response(x)
