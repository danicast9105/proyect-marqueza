import secrets
from datetime import datetime, timedelta

from Services.helpers import clean, execute, new_uuid, query, serialize_rows


class recuperacion_contrasena_services:
    @staticmethod
    def servListRecuperacion(id=None):
        rows = query(
            """SELECT r.REC_ID AS id, r.REC_UUID AS uuid, r.REC_CORREO AS correo,
                      u.USUA_NOMBRE AS usuario, r.REC_CREADO_EN AS creado_en,
                      r.REC_EXPIRA_EN AS expira_en, r.REC_USADO AS usado
               FROM T_RECUPERACION_CONTRASENA r
               JOIN T_USUARIOS u ON u.USUA_ID = r.REC_USUA_ID
               {where}
               ORDER BY r.REC_ID DESC"""
            .format(where="WHERE r.REC_ID = %s" if id is not None else ""),
            (id,) if id is not None else (),
        )
        return serialize_rows(rows)

    @staticmethod
    def addRecuperacionContrasena(data):
        correo = clean(data.get("correo"))
        if not correo:
            return {"mensaje": "El correo es obligatorio"}, 400

        usuarios = query(
            "SELECT USUA_ID FROM T_USUARIOS WHERE USUA_CORREO = %s LIMIT 1",
            (correo,),
        )
        if not usuarios:
            return {"mensaje": "No existe una cuenta con ese correo"}, 404

        token = secrets.token_urlsafe(32)
        execute(
            """INSERT INTO T_RECUPERACION_CONTRASENA
               (REC_UUID, REC_USUA_ID, REC_CORREO, REC_TOKEN, REC_EXPIRA_EN, REC_USADO)
               VALUES (%s, %s, %s, %s, %s, 0)""",
            (new_uuid(), usuarios[0]["USUA_ID"], correo, token,
             (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")),
        )
        return {"mensaje": "Solicitud de recuperacion registrada", "token": token}, 201

    @staticmethod
    def deleteRecuperacionContrasena(id):
        if not query("SELECT REC_ID FROM T_RECUPERACION_CONTRASENA WHERE REC_ID = %s", (id,)):
            return {"mensaje": "Recuperacion no encontrada"}, 404
        execute("DELETE FROM T_RECUPERACION_CONTRASENA WHERE REC_ID = %s", (id,))
        return {"mensaje": "Recuperacion eliminada correctamente"}, 200

    @staticmethod
    def updateRecuperacionContrasena(id, data):
        if not query("SELECT REC_ID FROM T_RECUPERACION_CONTRASENA WHERE REC_ID = %s", (id,)):
            return {"mensaje": "Recuperacion no encontrada"}, 404
        usado = data.get("usado")
        if usado not in (True, False, 0, 1):
            return {"mensaje": "El campo usado debe ser booleano"}, 400
        execute(
            """UPDATE T_RECUPERACION_CONTRASENA SET REC_USADO = %s WHERE REC_ID = %s""",
            (1 if usado else 0, id),
        )
        return {"mensaje": "Recuperacion actualizada correctamente"}, 200
