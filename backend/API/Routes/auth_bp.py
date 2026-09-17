import os
import secrets
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify, request


auth_bp = Blueprint("auth_bp", __name__)
_reset_tokens = {}


def send_reset_email(recipient, reset_url):
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SMTP_FROM", username)
    if not all((host, username, password, sender)):
        raise RuntimeError("SMTP no está configurado en el servidor.")

    message = EmailMessage()
    message["Subject"] = "Restablece tu contraseña | MARQUEZA"
    message["From"] = sender
    message["To"] = recipient
    message.set_content(
        "Hola,\n\n"
        "Recibimos una solicitud para cambiar tu contraseña de MARQUEZA. "
        f"Abre este enlace para continuar: {reset_url}\n\n"
        "Este enlace vence en 30 minutos. Si no realizaste esta solicitud, ignora este mensaje.\n\n"
        "MARQUEZA"
    )

    with smtplib.SMTP(host, port, timeout=15) as smtp:
        smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(message)


@auth_bp.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@auth_bp.route("/forgot-password", methods=["POST", "OPTIONS"])
def forgot_password():
    if request.method == "OPTIONS":
        return "", 204
    data = request.get_json(silent=True) or {}
    email = str(data.get("correo", "")).strip().lower()
    if not email or "@" not in email:
        return jsonify({"message": "Ingresa un correo electrónico válido."}), 400

    token = secrets.token_urlsafe(32)
    _reset_tokens[token] = {"correo": email, "expires": datetime.now(timezone.utc) + timedelta(minutes=30)}
    frontend_url = os.getenv("FRONTEND_RESET_URL", "http://localhost:5500/frontend/olvido_contrasena/restablecer.html")
    try:
        send_reset_email(email, f"{frontend_url}?token={token}")
    except RuntimeError as error:
        return jsonify({"message": str(error)}), 503
    except OSError:
        return jsonify({"message": "No fue posible conectar con el servidor de correo."}), 502

    return jsonify({"message": "Correo enviado correctamente."}), 200
