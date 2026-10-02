from flask import current_app
from Models.etc import ETC
import uuid as uuid_lib
from Services.validation import positive_id, required_fields

class etc_services:
    def servListETC(id=None):
        sql = "SELECT ETC_ID, ETC_UUID, ETC_NOMBRE FROM T_ESTADO_TIPOS_CATEGORIAS"
        if id is not None:
            sql += " WHERE ETC_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,) if id is not None else ())
        data = c.fetchall()
        etc_l = [ETC(u[0],u[1],u[2]).to_dic() for u in data]
        c.close()
        return etc_l

    def addETC(etc_nombre):
        error = required_fields({"etc_nombre": etc_nombre}, ("etc_nombre",))
        if error:
            return error
        uuid = str(uuid_lib.uuid4())
        sql = "INSERT INTO T_ESTADO_TIPOS_CATEGORIAS (ETC_UUID, ETC_NOMBRE) VALUES (%s, %s)"
        c = current_app.mysql.connection.cursor()
        c.execute(sql, (uuid, etc_nombre))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "ETC agregado correctamente"}

    def deleteETC(id):
        id = positive_id(id)
        if id is None:
            return {"mensaje": "El ID debe ser un entero positivo"}, 400
        sql = "DELETE FROM T_ESTADO_TIPOS_CATEGORIAS WHERE ETC_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute("SELECT ETC_ID FROM T_ESTADO_TIPOS_CATEGORIAS WHERE ETC_ID = %s", (id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Registro no encontrado"}, 404
        c.execute("SELECT DET_ETC_ID FROM T_DETALLES_ETC WHERE DET_ETC_ETC_ID = %s LIMIT 1", (id,))
        if c.fetchone():
            c.close()
            return {"mensaje": "El grupo tiene detalles asociados y no se puede eliminar"}, 409
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "ETC eliminado correctamente"}

    def updateETC(id, etc_nombre):
        id = positive_id(id)
        if id is None:
            return {"mensaje": "El ID debe ser un entero positivo"}, 400
        error = required_fields({"etc_nombre": etc_nombre}, ("etc_nombre",))
        if error:
            return error
        sql = "UPDATE T_ESTADO_TIPOS_CATEGORIAS SET ETC_NOMBRE = %s WHERE ETC_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute("SELECT ETC_ID FROM T_ESTADO_TIPOS_CATEGORIAS WHERE ETC_ID = %s", (id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Registro no encontrado"}, 404
        c.execute(sql, (etc_nombre, id))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "ETC actualizado correctamente"}
