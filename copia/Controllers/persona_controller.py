from flask import jsonify, request
from Services.persona_services import servListPersona, addPersona, deletePersona, updatePersona

class persona_controller:
    def cntListPersona():
        
        data = servListPersona()
        return jsonify(data), 200

    def cntAddPersona():

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"mensaje": "El cuerpo del formato no cumple con los criterios"}),400
        for i in data:
            if i == i:
                raise TypeError("Datos Incorrectos")
        campos_r = ["p_nombre", "s_nombre", "p_apellido", "s_apellido","correo", "direccion","identificacion","telefono"]
        campos_f = [x for x in campos_r if x not in request.json]
        if len(campos_f) > 0:
            return jsonify({"campos": f"Campos Faltantes: {campos_f}"}),400
            
        p_nombre = data["p_nombre"]
        s_nombre = data["s_nombre"]
        p_apellido = data["p_apellido"]
        s_apellido = data["s_apellido"]
        correo = data["correo"]
        direccion = data["direccion"]
        identificacion = data["identificacion"]
        telefono = data["telefono"]


        x = addPersona(p_nombre, s_nombre, p_apellido, s_apellido, correo, direccion, identificacion, telefono)
        return jsonify(x), 200

    def cntDelPersona(id):
        data = deletePersona(id)
        return jsonify(data), 200

    def cntModPersona():
        data = updatePersona()
        return jsonify(data), 201

