"""Creación y validación de tokens Bearer para las sesiones de la API."""
import base64
import binascii
import hashlib
import hmac
import json
import secrets
import time

from flask import current_app


class InvalidAccessToken(ValueError):
    """El token de acceso es inválido, expiró o fue revocado."""


class TokenConfigurationError(RuntimeError):
    """La configuración del token de acceso está incompleta."""


def _secret_bytes(secret):
    if not isinstance(secret, str) or len(secret) < 32:
        raise TokenConfigurationError(
            "Configura MARQUEZA_TOKEN_SECRET con una clave aleatoria de al menos 32 caracteres."
        )
    return secret.encode("utf-8")


def _encode(value):
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _decode(value):
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def create_access_token(subject, role, secret, ttl_seconds=None):
    if ttl_seconds is not None and (type(ttl_seconds) is not int or ttl_seconds <= 0):
        raise TokenConfigurationError("API_TOKEN_TTL_SECONDS debe ser un entero positivo.")

    now = int(time.time())
    payload = {
        "sub": str(subject),
        "role": str(role),
        "iat": now,
        "jti": secrets.token_urlsafe(16),
    }
    if ttl_seconds is not None:
        payload["exp"] = now + ttl_seconds
    encoded_payload = _encode(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    signature = hmac.new(_secret_bytes(secret), encoded_payload.encode("ascii"), hashlib.sha256).digest()
    return f"{encoded_payload}.{_encode(signature)}", payload["jti"]


def verify_access_token(token, secret, now=None):
    secret_bytes = _secret_bytes(secret)
    if not isinstance(token, str):
        raise InvalidAccessToken("Token inválido.")

    parts = token.split(".")
    if len(parts) != 2:
        raise InvalidAccessToken("Token inválido.")

    encoded_payload, encoded_signature = parts
    try:
        message = encoded_payload.encode("ascii")
        signature = _decode(encoded_signature)
        payload = json.loads(_decode(encoded_payload))
    except (binascii.Error, UnicodeError, ValueError) as error:
        raise InvalidAccessToken("Token inválido.") from error

    expected_signature = hmac.new(
        secret_bytes,
        message,
        hashlib.sha256,
    ).digest()
    if not hmac.compare_digest(signature, expected_signature):
        raise InvalidAccessToken("Token inválido.")

    if (
        not isinstance(payload, dict)
        or not isinstance(payload.get("sub"), str)
        or not payload["sub"]
        or not isinstance(payload.get("jti"), str)
        or not payload["jti"]
    ):
        raise InvalidAccessToken("Token inválido.")

    expiration = payload.get("exp")
    if expiration is not None and (
        type(expiration) is not int
        or expiration <= (int(time.time()) if now is None else now)
    ):
        raise InvalidAccessToken("Token inválido o expirado.")

    return payload


def _token_fingerprint(token_id):
    if not isinstance(token_id, str) or not token_id:
        raise InvalidAccessToken("Token inválido.")
    return hashlib.sha256(token_id.encode("utf-8")).hexdigest()


def ensure_access_token_table():
    if current_app.config.get("API_TOKEN_TABLE_READY"):
        return

    cursor = current_app.mysql.connection.cursor()
    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS T_API_TOKENS (
                   TOKEN_JTI_HASH CHAR(64) NOT NULL PRIMARY KEY,
                   TOKEN_USUA_ID INT NOT NULL,
                   TOKEN_CREADO TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                   TOKEN_REVOCADO TIMESTAMP NULL DEFAULT NULL,
                   INDEX IDX_API_TOKEN_USUARIO_ACTIVO (TOKEN_USUA_ID, TOKEN_REVOCADO),
                   CONSTRAINT FK_API_TOKEN_USUARIO
                       FOREIGN KEY (TOKEN_USUA_ID) REFERENCES T_USUARIOS (USUA_ID)
                       ON DELETE CASCADE
               ) ENGINE=InnoDB"""
        )
        current_app.mysql.connection.commit()
        current_app.config["API_TOKEN_TABLE_READY"] = True
    except Exception:
        current_app.mysql.connection.rollback()
        raise
    finally:
        cursor.close()


def register_access_token(token_id, user_id):
    ensure_access_token_table()
    cursor = current_app.mysql.connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO T_API_TOKENS (TOKEN_JTI_HASH, TOKEN_USUA_ID) VALUES (%s, %s)",
            (_token_fingerprint(token_id), user_id),
        )
        current_app.mysql.connection.commit()
    except Exception:
        current_app.mysql.connection.rollback()
        raise
    finally:
        cursor.close()


def is_access_token_active(token_id):
    cursor = current_app.mysql.connection.cursor()
    try:
        cursor.execute(
            """SELECT 1
               FROM T_API_TOKENS t
               JOIN T_USUARIOS u ON u.USUA_ID = t.TOKEN_USUA_ID
               WHERE t.TOKEN_JTI_HASH = %s
                 AND t.TOKEN_REVOCADO IS NULL
                 AND u.USUA_ESTADO = 'Activo'
               LIMIT 1""",
            (_token_fingerprint(token_id),),
        )
        return cursor.fetchone() is not None
    finally:
        cursor.close()


def revoke_access_token(token_id):
    cursor = current_app.mysql.connection.cursor()
    try:
        cursor.execute(
            """UPDATE T_API_TOKENS
               SET TOKEN_REVOCADO = CURRENT_TIMESTAMP
               WHERE TOKEN_JTI_HASH = %s AND TOKEN_REVOCADO IS NULL""",
            (_token_fingerprint(token_id),),
        )
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception:
        current_app.mysql.connection.rollback()
        raise
    finally:
        cursor.close()
