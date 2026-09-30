import secrets
from datetime import datetime, timedelta

from Services.helpers import clean, execute, new_uuid, query, serialize_rows


class recuperacion_contrasena_services:
    @staticmethod
    def servListRecuperacion():
        rows = query(
            """SELECT r.REC_ID AS id, r.REC_UUID AS uuid, r.REC_CORREO AS correo,
                      u.USUA_NOMBRE AS usuario, r.REC_CREADO_EN AS creado_en,
                      r.REC_EXPIRA_EN AS expira_en, r.REC_USADO AS usado
               FROM t_recuperacion_contrasena r
               JOIN t_usuarios u ON u.USUA_ID = r.REC_USUA_ID
               ORDER BY r.REC_ID DESC"""
        )
        return serialize_rows(rows)

    @staticmethod
    def addRecuperacionContrasena(data):
        correo = clean(data.get("correo"))
        if not correo:
            return {"mensaje": "El correo es obligatorio"}, 400

        usuarios = query(
            "SELECT USUA_ID FROM t_usuarios WHERE USUA_CORREO = %s LIMIT 1",
            (correo,),
        )
        if not usuarios:
            return {"mensaje": "No existe una cuenta con ese correo"}, 404

        token = secrets.token_urlsafe(32)
        execute(
            """INSERT INTO t_recuperacion_contrasena
               (REC_UUID, REC_USUA_ID, REC_CORREO, REC_TOKEN, REC_EXPIRA_EN, REC_USADO)
               VALUES (%s, %s, %s, %s, %s, 0)""",
            (new_uuid(), usuarios[0]["USUA_ID"], correo, token,
             (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")),
        )
        return {"mensaje": "Solicitud de recuperacion registrada", "token": token}, 201

    @staticmethod
    def deleteRecuperacionContrasena(id):
        execute("DELETE FROM t_recuperacion_contrasena WHERE REC_ID = %s", (id,))
        return {"mensaje": "Recuperacion eliminada correctamente"}, 200

    @staticmethod
    def updateRecuperacionContrasena(id, data):
        execute(
            """UPDATE t_recuperacion_contrasena SET REC_USADO = %s WHERE REC_ID = %s""",
            (1 if data.get("usado") else 0, id),
        )
        return {"mensaje": "Recuperacion actualizada correctamente"}, 200
