import secrets
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
from flask import Blueprint, jsonify, request, current_app

from Services.helpers import hash_password, query, verify_password

auth_bp = Blueprint("auth_bp", __name__)
_reset_tokens = {}


def send_reset_email(recipient, reset_url):
    config = current_app.config
    host = config.get("SMTP_HOST")
    port = config.get("SMTP_PORT", 587)
    username = config.get("SMTP_USERNAME")
    password = config.get("SMTP_PASSWORD")
    sender = config.get("SMTP_FROM") or username
    use_ssl = config.get("SMTP_USE_SSL", port == 465)
    timeout = config.get("SMTP_TIMEOUT", 15)
    if not all((host, username, password, sender)):
        raise RuntimeError("Configura SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD y SMTP_FROM en el backend.")
    if host.lower() == "smtp.gmail.com":
        password = "".join(password.split())
        if len(password) != 16:
            raise RuntimeError(
                "SMTP_PASSWORD de Gmail debe ser una contraseña de aplicación de 16 caracteres; no uses la contraseña normal de tu cuenta."
            )

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

    tls_context = ssl.create_default_context()
    if use_ssl:
        smtp_connection = smtplib.SMTP_SSL(host, port, timeout=timeout, context=tls_context)
    else:
        smtp_connection = smtplib.SMTP(host, port, timeout=timeout)

    with smtp_connection as smtp:
        if not use_ssl:
            smtp.starttls(context=tls_context)
        smtp.login(username, password)
        smtp.send_message(message)


@auth_bp.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@auth_bp.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return "", 204
    data = request.get_json(silent=True) or {}
    identificador = str(data.get("correo") or data.get("usuario") or "").strip()
    contrasena = data.get("contrasena") or data.get("password") or ""

    if not identificador:
        return jsonify({"message": "Ingresa tu usuario o correo."}), 400
    if not contrasena:
        return jsonify({"message": "Ingresa tu contrasena."}), 400

    usuarios = query(
        """SELECT u.USUA_ID, u.USUA_NOMBRE, u.USUA_CORREO, u.USUA_CONTRASENA,
                  u.USUA_ESTADO, u.USUA_DET_ETC_ID, d.DET_ETC_NOMBRE
           FROM t_usuarios u
           JOIN t_detalles_etc d ON d.DET_ETC_ID = u.USUA_DET_ETC_ID
           WHERE u.USUA_CORREO = %s OR u.USUA_NOMBRE = %s
           LIMIT 1""",
        (identificador, identificador),
    )
    if not usuarios:
        return jsonify({"message": "Usuario o contrasena incorrectos."}), 401

    usuario = usuarios[0]
    if usuario["USUA_ESTADO"] != "Activo":
        return jsonify({"message": "La cuenta esta desactivada."}), 403
    if not verify_password(usuario["USUA_CONTRASENA"], contrasena):
        return jsonify({"message": "Usuario o contrasena incorrectos."}), 401

    from Services.usuarios_services import marcar_ultimo_acceso
    try:
        marcar_ultimo_acceso(usuario["USUA_ID"])
    except Exception:
        pass

    token = secrets.token_urlsafe(32)

    return jsonify({
        "message": "Inicio de sesion exitoso",
        "token": token,
        "usuario": {
            "id": usuario["USUA_ID"],
            "nombre": usuario["USUA_NOMBRE"],
            "correo": usuario["USUA_CORREO"],
            "rol": usuario["DET_ETC_NOMBRE"],
            "rol_id": usuario["USUA_DET_ETC_ID"]
        }
    }), 200


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
    frontend_url = current_app.config.get("FRONTEND_RESET_URL")
    separator = "&" if "?" in frontend_url else "?"
    reset_url = f"{frontend_url}{separator}{urlencode({'token': token})}"
    try:
        send_reset_email(email, reset_url)
    except RuntimeError as error:
        _reset_tokens.pop(token, None)
        return jsonify({"message": str(error)}), 503
    except smtplib.SMTPAuthenticationError:
        _reset_tokens.pop(token, None)
        current_app.logger.warning("El proveedor SMTP rechazó la autenticación.")
        return jsonify({
            "message": "Gmail rechazó la autenticación. Verifica el usuario y que SMTP_PASSWORD sea una contraseña de aplicación vigente."
        }), 502
    except smtplib.SMTPServerDisconnected:
        _reset_tokens.pop(token, None)
        current_app.logger.warning("El servidor SMTP cerró la conexión durante el envío.")
        if current_app.config.get("SMTP_HOST", "").lower() == "smtp.gmail.com":
            message = "Gmail cerró la conexión durante la autenticación. Revisa la contraseña de aplicación de 16 caracteres y que la verificación en dos pasos esté activa."
        else:
            message = "El servidor SMTP cerró la conexión. Verifica host, puerto y credenciales SMTP."
        return jsonify({"message": message}), 502
    except (OSError, smtplib.SMTPException):
        _reset_tokens.pop(token, None)
        return jsonify({"message": "No fue posible conectar con el servidor de correo."}), 502

    return jsonify({"message": "Correo enviado correctamente."}), 200


@auth_bp.route("/reset-password", methods=["POST", "OPTIONS"])
def reset_password():
    if request.method == "OPTIONS":
        return "", 204
    data = request.get_json(silent=True) or {}
    token = data.get("token", "")
    new_password = data.get("nueva_contrasena", "")

    if not token or not new_password:
        return jsonify({"message": "Token y nueva contraseña son requeridos."}), 400

    if token not in _reset_tokens:
        return jsonify({"message": "Token inválido o expirado."}), 400

    token_data = _reset_tokens[token]
    if datetime.now(timezone.utc) > token_data["expires"]:
        del _reset_tokens[token]
        return jsonify({"message": "Token expirado."}), 400

    correo = token_data["correo"]
    c = current_app.mysql.connection.cursor()
    c.execute("SELECT USUA_ID FROM T_USUARIOS WHERE USUA_CORREO = %s", (correo,))
    user = c.fetchone()
    if not user:
        c.close()
        return jsonify({"message": "Usuario no encontrado."}), 404

    usua_id = user[0]
    c.execute("UPDATE T_USUARIOS SET USUA_CONTRASENA = %s WHERE USUA_ID = %s",
              (hash_password(new_password), usua_id))
    current_app.mysql.connection.commit()
    c.close()

    del _reset_tokens[token]
    return jsonify({"message": "Contraseña actualizada correctamente."}), 200
