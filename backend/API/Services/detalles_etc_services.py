from flask import current_app
from Models.detalles_etc import Detalles_etc
import uuid as uuid_lib
from Services.validation import positive_id, required_fields

class detalles_etc_services:
    def servListDetalles_etc(id=None):
        sql = "SELECT DET_ETC_ID, DET_ETC_UUID, DET_ETC_NOMBRE, DET_ETC_ETC_ID, DET_ETC_PER_ID FROM T_DETALLES_ETC"
        if id is not None:
            sql += " WHERE DET_ETC_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,) if id is not None else ())
        data = c.fetchall()
        detalles_etc_l = [Detalles_etc(u[0],u[1],u[2],u[3],u[4]).to_dic() for u in data]
        c.close()
        return detalles_etc_l

    def addDetalles_etc(det_etc_nombre, det_etc_etc_id, det_etc_per_id):
        error = required_fields(
            {"det_etc_nombre": det_etc_nombre, "det_etc_etc_id": det_etc_etc_id},
            ("det_etc_nombre", "det_etc_etc_id"),
        )
        if error:
            return error
        det_etc_etc_id = positive_id(det_etc_etc_id)
        if det_etc_etc_id is None:
            return {"mensaje": "El grupo debe ser un ID entero positivo"}, 400
        c = current_app.mysql.connection.cursor()
        c.execute(
            "SELECT ETC_ID FROM T_ESTADO_TIPOS_CATEGORIAS WHERE ETC_ID = %s",
            (det_etc_etc_id,),
        )
        if not c.fetchone():
            c.close()
            return {"mensaje": "Grupo no encontrado"}, 404
        if det_etc_per_id not in (None, ""):
            det_etc_per_id = positive_id(det_etc_per_id)
            if det_etc_per_id is None:
                c.close()
                return {"mensaje": "La persona debe ser un ID entero positivo"}, 400
            c.execute("SELECT PER_ID FROM T_PERSONA WHERE PER_ID = %s", (det_etc_per_id,))
            if not c.fetchone():
                c.close()
                return {"mensaje": "Persona no encontrada"}, 404
        c.close()
        uuid = str(uuid_lib.uuid4())
        sql = "INSERT INTO T_DETALLES_ETC (DET_ETC_UUID, DET_ETC_NOMBRE, DET_ETC_ETC_ID, DET_ETC_PER_ID) VALUES (%s, %s, %s, %s)"
        c = current_app.mysql.connection.cursor()
        c.execute(sql, (uuid, det_etc_nombre, det_etc_etc_id, det_etc_per_id))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Detalle agregado correctamente"}

    def deleteDetalles_etc(id):
        id = positive_id(id)
        if id is None:
            return {"mensaje": "El ID debe ser un entero positivo"}, 400
        sql = "DELETE FROM T_DETALLES_ETC WHERE DET_ETC_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute("SELECT DET_ETC_ID FROM T_DETALLES_ETC WHERE DET_ETC_ID = %s", (id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Detalle no encontrado"}, 404
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Detalle eliminado correctamente"}

    def updateDetalles_etc(id, det_etc_nombre, det_etc_etc_id, det_etc_per_id):
        id = positive_id(id)
        if id is None:
            return {"mensaje": "El ID debe ser un entero positivo"}, 400
        error = required_fields(
            {"det_etc_nombre": det_etc_nombre, "det_etc_etc_id": det_etc_etc_id},
            ("det_etc_nombre", "det_etc_etc_id"),
        )
        if error:
            return error
        det_etc_etc_id = positive_id(det_etc_etc_id)
        if det_etc_etc_id is None:
            return {"mensaje": "El grupo debe ser un ID entero positivo"}, 400
        c = current_app.mysql.connection.cursor()
        c.execute(
            "SELECT ETC_ID FROM T_ESTADO_TIPOS_CATEGORIAS WHERE ETC_ID = %s",
            (det_etc_etc_id,),
        )
        if not c.fetchone():
            c.close()
            return {"mensaje": "Grupo no encontrado"}, 404
        if det_etc_per_id not in (None, ""):
            det_etc_per_id = positive_id(det_etc_per_id)
            if det_etc_per_id is None:
                c.close()
                return {"mensaje": "La persona debe ser un ID entero positivo"}, 400
            c.execute("SELECT PER_ID FROM T_PERSONA WHERE PER_ID = %s", (det_etc_per_id,))
            if not c.fetchone():
                c.close()
                return {"mensaje": "Persona no encontrada"}, 404
        c.close()
        sql = "UPDATE T_DETALLES_ETC SET DET_ETC_NOMBRE = %s, DET_ETC_ETC_ID = %s, DET_ETC_PER_ID = %s WHERE DET_ETC_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute("SELECT DET_ETC_ID FROM T_DETALLES_ETC WHERE DET_ETC_ID = %s", (id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Detalle no encontrado"}, 404
        c.execute(sql, (det_etc_nombre, det_etc_etc_id, det_etc_per_id, id))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Detalle actualizado correctamente"}
