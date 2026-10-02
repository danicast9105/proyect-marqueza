from flask import current_app
from Models.contacto import Contacto
import uuid as uuid_lib
from Services.validation import positive_id, required_fields

class contacto_services:
    def servListContacto(id=None):
        sql = "SELECT * FROM T_CONTACTO"
        if id is not None:
            sql += " WHERE CONT_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,) if id is not None else ())
        data = c.fetchall()
        contactos_l = [Contacto(u[0],u[1],u[2],u[3],u[4]).to_dic() for u in data]
        c.close()
        return contactos_l

    def addContacto(tipo_contacto, contenido, proveedor_id):
        error = required_fields(
            {"tipo_contacto": tipo_contacto, "contenido": contenido, "proveedor_id": proveedor_id},
            ("tipo_contacto", "contenido", "proveedor_id"),
        )
        if error:
            return error
        proveedor_id = positive_id(proveedor_id)
        if proveedor_id is None:
            return {"mensaje": "El proveedor_id debe ser un entero positivo"}, 400
        uuid = str(uuid_lib.uuid4())
        sql = "INSERT INTO T_CONTACTO (CONT_UUID, CONT_TIPO_DATO, CONT_CONTENIDO, CONT_PROV_ID) VALUES (%s, %s, %s, %s)"
        c = current_app.mysql.connection.cursor()
        c.execute("SELECT PROV_ID FROM T_PROVEEDORES WHERE PROV_ID = %s", (proveedor_id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Proveedor no encontrado"}, 404
        c.execute(sql, (uuid, tipo_contacto, contenido, proveedor_id))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Contacto agregado correctamente"}

    def deleteContacto(id):
        id = positive_id(id)
        if id is None:
            return {"mensaje": "El ID debe ser un entero positivo"}, 400
        sql = "DELETE FROM T_CONTACTO WHERE CONT_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute("SELECT CONT_ID FROM T_CONTACTO WHERE CONT_ID = %s", (id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Contacto no encontrado"}, 404
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Contacto eliminado correctamente"}

    def updateContacto(id, tipo_contacto, contenido, proveedor_id):
        id = positive_id(id)
        if id is None:
            return {"mensaje": "El ID debe ser un entero positivo"}, 400
        error = required_fields(
            {"tipo_contacto": tipo_contacto, "contenido": contenido, "proveedor_id": proveedor_id},
            ("tipo_contacto", "contenido", "proveedor_id"),
        )
        if error:
            return error
        proveedor_id = positive_id(proveedor_id)
        if proveedor_id is None:
            return {"mensaje": "El proveedor_id debe ser un entero positivo"}, 400
        sql = "UPDATE T_CONTACTO SET CONT_TIPO_DATO = %s, CONT_CONTENIDO = %s, CONT_PROV_ID = %s WHERE CONT_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute("SELECT CONT_ID FROM T_CONTACTO WHERE CONT_ID = %s", (id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Contacto no encontrado"}, 404
        c.execute("SELECT PROV_ID FROM T_PROVEEDORES WHERE PROV_ID = %s", (proveedor_id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Proveedor no encontrado"}, 404
        c.execute(sql, (tipo_contacto, contenido, proveedor_id, id))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Contacto actualizado correctamente"}
