import uuid as uuid_lib
from datetime import datetime, timezone

from Services.helpers import clean, execute, query, serialize_rows

_OUTCOMES = ("success", "denied", "error")

_ALIASES = {
    "uuid": ("uuid", "id"),
    "timestamp": ("timestamp", "fecha_hora"),
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


def _event_timestamp(value):
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


class bitacora_auditoria_services:
    @staticmethod
    def servListBitacora(id=None):
        rows = query(
            """SELECT AUD_FECHA_HORA AS timestamp, AUD_UUID AS uuid,
                      AUD_ACTOR AS actor, AUD_CORREO AS email, AUD_ROL AS role,
                      AUD_ACCION AS action, AUD_MODULO AS module, AUD_ENTIDAD AS entity,
                      AUD_DETALLE AS detail, AUD_RESULTADO AS outcome, AUD_ID AS id
               FROM T_BITACORA_AUDITORIA
               {where}
               ORDER BY AUD_FECHA_HORA DESC, AUD_ID DESC
               """
            .format(where="WHERE AUD_ID = %s" if id is not None else ""),
            (id,) if id is not None else (),
        )
        serialized = serialize_rows(rows)
        for row, source in zip(serialized, rows):
            timestamp = source.get("timestamp")
            if isinstance(timestamp, datetime):
                row["timestamp"] = (
                    timestamp.replace(tzinfo=timezone.utc)
                    .isoformat(timespec="seconds")
                    .replace("+00:00", "Z")
                )
        return serialized

    @staticmethod
    def addBitacoraAuditoria(data):
        event_uuid = str(clean(_pick(data, "uuid")) or uuid_lib.uuid4().hex)
        timestamp = _event_timestamp(_pick(data, "timestamp"))
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
            """INSERT INTO T_BITACORA_AUDITORIA
               (AUD_UUID, AUD_FECHA_HORA, AUD_ACTOR, AUD_CORREO, AUD_ROL, AUD_ACCION,
                AUD_MODULO, AUD_ENTIDAD, AUD_DETALLE, AUD_RESULTADO)
               VALUES (%s, COALESCE(%s, CURRENT_TIMESTAMP), %s, %s, %s, %s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE AUD_UUID = AUD_UUID""",
            (event_uuid[:80], timestamp, actor, email, role, action[:100], module[:80],
             entity[:150] if entity else None, detail, outcome),
        )
        return {"mensaje": "Bitacora de auditoria registrada correctamente"}, 201

    @staticmethod
    def deleteBitacoraAuditoria(id):
        if not query("SELECT AUD_ID FROM T_BITACORA_AUDITORIA WHERE AUD_ID = %s", (id,)):
            return {"mensaje": "Registro de bitacora no encontrado"}, 404
        execute("DELETE FROM T_BITACORA_AUDITORIA WHERE AUD_ID = %s", (id,))
        return {"mensaje": "Bitacora eliminada correctamente"}, 200

    @staticmethod
    def updateBitacoraAuditoria(id, data):
        if not query("SELECT AUD_ID FROM T_BITACORA_AUDITORIA WHERE AUD_ID = %s", (id,)):
            return {"mensaje": "Registro de bitacora no encontrado"}, 404
        outcome = clean(_pick(data, "outcome"), "success")
        if outcome not in _OUTCOMES:
            return {"mensaje": "El resultado indicado no es valido"}, 400
        execute(
            """UPDATE T_BITACORA_AUDITORIA SET AUD_ACTOR = %s, AUD_CORREO = %s, AUD_ROL = %s,
               AUD_ACCION = %s, AUD_MODULO = %s, AUD_ENTIDAD = %s, AUD_DETALLE = %s,
               AUD_RESULTADO = %s
               WHERE AUD_ID = %s""",
            (clean(_pick(data, "actor"), "Sin identificar"), clean(_pick(data, "email")) or None,
             clean(_pick(data, "role")) or None, clean(_pick(data, "action")) or "Actividad",
             clean(_pick(data, "module"), "Sistema"), clean(_pick(data, "entity")) or None,
             clean(_pick(data, "detail")) or None, outcome, id),
        )
        return {"mensaje": "Bitacora actualizada correctamente"}, 200
