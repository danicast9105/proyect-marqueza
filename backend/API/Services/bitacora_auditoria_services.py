import time
import uuid as uuid_lib

from Services.helpers import clean, execute, query, serialize_rows

_OUTCOMES = ("success", "denied", "error")

_ALIASES = {
    "actor": ("actor", "usuario", "nombre"),
    "email": ("email", "correo"),
    "role": ("role", "rol"),
    "action": ("action", "accion"),
    "module": ("module", "modulo"),
    "entity": ("entity", "entidad"),
    "detail": ("detail", "detalle"),
    "outcome": ("outcome", "resultado"),
}


def _pick(data, key):
    for candidate in _ALIASES[key]:
        value = data.get(candidate)
        if value not in (None, ""):
            return value
    return ""


class bitacora_auditoria_services:
    @staticmethod
    def servListBitacora():
        rows = query(
            """SELECT AUD_FECHA_HORA AS timestamp, AUD_FECHA_HORA AS fecha_hora,
                      AUD_ACTOR AS actor, AUD_CORREO AS email, AUD_ROL AS role,
                      AUD_ACCION AS action, AUD_MODULO AS module, AUD_ENTIDAD AS entity,
                      AUD_DETALLE AS detail, AUD_RESULTADO AS outcome, AUD_ID AS id
               FROM t_bitacora_auditoria
               ORDER BY AUD_FECHA_HORA DESC, AUD_ID DESC
               LIMIT 1000"""
        )
        return serialize_rows(rows)

    @staticmethod
    def addBitacoraAuditoria(data):
        actor = clean(_pick(data, "actor"), "Sin identificar")
        email = clean(_pick(data, "email")) or None
        role = clean(_pick(data, "role")) or None
        action = clean(_pick(data, "action")) or "Actividad"
        module = clean(_pick(data, "module"), "Sistema")
        entity = clean(_pick(data, "entity")) or None
        detail = clean(_pick(data, "detail")) or None
        outcome = clean(_pick(data, "outcome"), "success")
        if outcome not in _OUTCOMES:
            outcome = "success"

        execute(
            """INSERT INTO t_bitacora_auditoria
               (AUD_UUID, AUD_ACTOR, AUD_CORREO, AUD_ROL, AUD_ACCION, AUD_MODULO,
                AUD_ENTIDAD, AUD_DETALLE, AUD_RESULTADO)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (f"{int(time.time() * 1000)}-{uuid_lib.uuid4().hex[:12]}", actor, email, role,
             action[:100], module[:80], entity[:150] if entity else None, detail, outcome),
        )
        return {"mensaje": "Bitacora de auditoria registrada correctamente"}, 201

    @staticmethod
    def deleteBitacoraAuditoria(id):
        execute("DELETE FROM t_bitacora_auditoria WHERE AUD_ID = %s", (id,))
        return {"mensaje": "Bitacora eliminada correctamente"}, 200

    @staticmethod
    def updateBitacoraAuditoria(id, data):
        execute(
            """UPDATE t_bitacora_auditoria SET AUD_ACTOR = %s, AUD_CORREO = %s, AUD_ROL = %s,
               AUD_ACCION = %s, AUD_MODULO = %s, AUD_ENTIDAD = %s, AUD_DETALLE = %s,
               AUD_RESULTADO = %s
               WHERE AUD_ID = %s""",
            (clean(_pick(data, "actor"), "Sin identificar"), clean(_pick(data, "email")) or None,
             clean(_pick(data, "role")) or None, clean(_pick(data, "action")) or "Actividad",
             clean(_pick(data, "module"), "Sistema"), clean(_pick(data, "entity")) or None,
             clean(_pick(data, "detail")) or None, clean(_pick(data, "outcome"), "success"), id),
        )
        return {"mensaje": "Bitacora actualizada correctamente"}, 200
