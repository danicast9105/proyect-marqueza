from flask import current_app
from Models.persona import Persona
import uuid as uuid_lib
from Services.validation import positive_id, required_fields

class persona_services:
    def servListPersona(id=None):
        sql = "SELECT PER_ID, PER_UUID, PER_NOMBRE, PER_SEG_NOMBRE, PER_PRI_APELLIDO, PER_SEG_APELLIDO, PER_CORREO, PER_DIRECCION, PER_IDENTIFICACION, PER_TELEFONO FROM T_PERSONA"
        if id is not None:
            sql += " WHERE PER_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,) if id is not None else ())
        data = c.fetchall()
        personas_l = [Persona(u[0],u[1],u[2],u[3],u[4],u[5],u[6],u[7],u[8],u[9]).to_dic() for u in data]
        c.close()
        return personas_l

    def addPersona(nombre, seg_nombre, pri_apellido, seg_apellido, correo, direccion, identificacion, telefono):
        error = required_fields(
            {"nombre": nombre, "identificacion": identificacion},
            ("nombre", "identificacion"),
        )
        if error:
            return error
        c = current_app.mysql.connection.cursor()
        c.execute(
            "SELECT PER_ID FROM T_PERSONA WHERE PER_IDENTIFICACION = %s",
            (identificacion,),
        )
        if c.fetchone():
            c.close()
            return {"mensaje": "Ya existe una persona con esa identificacion"}, 409
        c.close()
        uuid = str(uuid_lib.uuid4())
        sql = "INSERT INTO T_PERSONA (PER_UUID, PER_NOMBRE, PER_SEG_NOMBRE, PER_PRI_APELLIDO, PER_SEG_APELLIDO, PER_CORREO, PER_DIRECCION, PER_IDENTIFICACION, PER_TELEFONO) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        c = current_app.mysql.connection.cursor()
        c.execute(sql, (uuid, nombre, seg_nombre, pri_apellido, seg_apellido, correo, direccion, identificacion, telefono))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Persona agregada correctamente"}

    def deletePersona(id):
        id = positive_id(id)
        if id is None:
            return {"mensaje": "El ID debe ser un entero positivo"}, 400
        sql = "DELETE FROM T_PERSONA WHERE PER_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute("SELECT PER_ID FROM T_PERSONA WHERE PER_ID = %s", (id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Persona no encontrada"}, 404
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Persona eliminada correctamente"}

    def updatePersona(id, nombre, seg_nombre, pri_apellido, seg_apellido, correo, direccion, identificacion, telefono):
        id = positive_id(id)
        if id is None:
            return {"mensaje": "El ID debe ser un entero positivo"}, 400
        error = required_fields(
            {"nombre": nombre, "identificacion": identificacion},
            ("nombre", "identificacion"),
        )
        if error:
            return error
        sql = "UPDATE T_PERSONA SET PER_NOMBRE = %s, PER_SEG_NOMBRE = %s, PER_PRI_APELLIDO = %s, PER_SEG_APELLIDO = %s, PER_CORREO = %s, PER_DIRECCION = %s, PER_IDENTIFICACION = %s, PER_TELEFONO = %s WHERE PER_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute("SELECT PER_ID FROM T_PERSONA WHERE PER_ID = %s", (id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Persona no encontrada"}, 404
        c.execute(
            "SELECT PER_ID FROM T_PERSONA WHERE PER_IDENTIFICACION = %s AND PER_ID <> %s",
            (identificacion, id),
        )
        if c.fetchone():
            c.close()
            return {"mensaje": "Ya existe una persona con esa identificacion"}, 409
        c.execute(sql, (nombre, seg_nombre, pri_apellido, seg_apellido, correo, direccion, identificacion, telefono, id))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Persona actualizada correctamente"}
