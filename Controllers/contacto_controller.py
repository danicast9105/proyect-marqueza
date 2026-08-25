from flask import jsonify, request
from Services.contacto_services import contacto_services

class contacto_controller:
    def cntListContacto():
        data = contacto_services.servListContacto()
        return jsonify(data), 200

    def cntAddContacto():
        tipo_contacto = request.json["tipo_contacto"]
        contenido = request.json["contenido"]
        proveedor_id = request.json["proveedor_id"]

        data = contacto_services.addContacto(tipo_contacto, contenido, proveedor_id)
        return jsonify(data), 200

    def cntDelContacto():
        data = contacto_services.deleteContacto()
        return jsonify(data), 200

    def cntModContacto():
        data = contacto_services.updateContacto()
        return jsonify(data), 201

