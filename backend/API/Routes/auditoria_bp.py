from datetime import datetime, timezone
from uuid import uuid4

from flask import Blueprint, jsonify, request
from sqlalchemy import select

from orm import orm_model, orm_session


auditoria_bp = Blueprint("auditoria_bp", __name__)


@auditoria_bp.route("/", methods=["GET"])
def list_events():
    model = orm_model("t_auditoria_ui")
    with orm_session() as session:
        rows = session.scalars(
            select(model).order_by(model.AUD_TIMESTAMP.desc(), model.AUD_ID.desc()).limit(500)
        ).all()
        events = []
        for row in rows:
            events.append({
                "id": row.AUD_UUID,
                "timestamp": row.AUD_TIMESTAMP.isoformat(),
                "actor": row.AUD_ACTOR,
                "email": row.AUD_EMAIL,
                "role": row.AUD_ROLE,
                "action": row.AUD_ACTION,
                "module": row.AUD_MODULE,
                "entity": row.AUD_ENTITY,
                "detail": row.AUD_DETAIL,
                "outcome": row.AUD_OUTCOME,
            })
        return jsonify(events), 200


@auditoria_bp.route("/", methods=["POST"])
def create_event():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not payload.get("action") or not payload.get("detail"):
        return jsonify({"error": "action y detail son obligatorios."}), 400

    raw_timestamp = str(payload.get("timestamp") or "")
    try:
        timestamp = datetime.fromisoformat(raw_timestamp.replace("Z", "+00:00"))
    except ValueError:
        timestamp = datetime.now(timezone.utc)
    if timestamp.tzinfo is not None:
        timestamp = timestamp.astimezone(timezone.utc).replace(tzinfo=None)

    model = orm_model("t_auditoria_ui")
    with orm_session() as session:
        event = model(
            AUD_UUID=str(payload.get("id") or uuid4()),
            AUD_TIMESTAMP=timestamp,
            AUD_ACTOR=str(payload.get("actor") or "Sin identificar")[:60],
            AUD_EMAIL=str(payload.get("email") or "")[:100],
            AUD_ROLE=str(payload.get("role") or "")[:45],
            AUD_ACTION=str(payload["action"])[:100],
            AUD_MODULE=str(payload.get("module") or "Sistema")[:80],
            AUD_ENTITY=str(payload.get("entity") or "")[:160],
            AUD_DETAIL=str(payload["detail"]),
            AUD_OUTCOME=str(payload.get("outcome") or "success")[:20],
        )
        session.add(event)
        return jsonify({"id": event.AUD_UUID}), 201