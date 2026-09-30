"""Utilidades compartidas por los Services de MARQUEZA."""
import uuid as uuid_lib
from datetime import date, datetime, time
from decimal import Decimal

import bcrypt
from flask import current_app
from werkzeug.security import check_password_hash


def new_uuid():
    return str(uuid_lib.uuid4())


def connection():
    return current_app.mysql.connection


def _rollback():
    try:
        current_app.mysql.connection.rollback()
    except Exception:
        pass


def query(sql, params=()):
    """Ejecuta SELECT y devuelve filas como diccionarios (nombres de columna reales)."""
    c = current_app.mysql.connection.cursor()
    try:
        c.execute(sql, params)
        rows = c.fetchall()
        columns = [d[0] for d in c.description] if c.description else []
        return [dict(zip(columns, row)) for row in rows]
    except Exception:
        _rollback()
        raise
    finally:
        c.close()


def scalar(sql, params=()):
    c = current_app.mysql.connection.cursor()
    try:
        c.execute(sql, params)
        row = c.fetchone()
        return row[0] if row else None
    except Exception:
        _rollback()
        raise
    finally:
        c.close()


def execute(sql, params=()):
    """Ejecuta INSERT/UPDATE/DELETE y confirma. Devuelve lastrowid."""
    c = current_app.mysql.connection.cursor()
    try:
        c.execute(sql, params)
        current_app.mysql.connection.commit()
        return c.lastrowid
    except Exception:
        _rollback()
        raise
    finally:
        c.close()


def serialize(value):
    if isinstance(value, datetime):
        if value.time() == time(0, 0, 0):
            return value.date().isoformat()
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (bytes, bytearray)):
        return value.decode("utf-8", "replace")
    return value


def serialize_rows(rows):
    return [{k: serialize(v) for k, v in row.items()} for row in rows]


def clean(value, default=None):
    if value is None:
        return default
    if isinstance(value, str):
        value = value.strip()
        return value if value else default
    return value


def unique_identificacion(value=None):
    """PER_IDENTIFICACION es NOT NULL + UNIQUE: nunca debe quedar vacio."""
    value = clean(value)
    if value:
        return value
    return f"SIN-{new_uuid()[:20].upper()}"


def hash_password(raw):
    if raw is None or raw == "":
        return None
    return bcrypt.hashpw(str(raw).encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")


def verify_password(stored, raw):
    """Verifica bcrypt ($2a/$2b/$2y), hashes de Werkzeug y (legado) texto plano."""
    if not stored:
        return False
    stored_text = str(stored)
    raw_text = str(raw or "")
    try:
        if stored_text.startswith(("$2a$", "$2b$", "$2y$")):
            return bcrypt.checkpw(raw_text.encode("utf-8"), stored_text.encode("utf-8"))
        if stored_text.startswith(("pbkdf2:", "scrypt:", "argon2")):
            return check_password_hash(stored_text, raw_text)
        return stored_text == raw_text
    except Exception:
        return False


# ------------------------------------------------------------------
# Resolventes de relaciones (el frontend envía nombres, la BD ids)
# ------------------------------------------------------------------
def resolve_categoria(nombre, grupo):
    if not nombre:
        return None
    return scalar(
        """SELECT d.DET_ETC_ID
           FROM t_detalles_etc d
           JOIN t_estado_tipos_categorias e ON e.ETC_ID = d.DET_ETC_ETC_ID
           WHERE d.DET_ETC_NOMBRE = %s AND e.ETC_NOMBRE = %s
           LIMIT 1""",
        (nombre, grupo),
    )


def resolve_rol(nombre):
    return resolve_categoria(nombre, "ROLES_USUARIO")


def resolve_proveedor(empresa):
    if not empresa:
        return None
    prov_id = scalar("SELECT PROV_ID FROM t_proveedores WHERE PROV_EMPRESA = %s LIMIT 1", (empresa,))
    if prov_id is not None:
        return prov_id
    return scalar(
        """SELECT p.PROV_ID FROM t_proveedores p
           JOIN t_persona per ON per.PER_ID = p.PROV_PER_ID
           WHERE %s <> '' AND (p.PROV_EMPRESA = %s OR per.PER_NOMBRE = %s)
           LIMIT 1""",
        (empresa, empresa, empresa),
    )


def resolve_cliente(nombre_o_documento):
    """Devuelve CLI_ID buscando por nombre completo (vista) o por documento."""
    if not nombre_o_documento:
        return None
    return scalar(
        """SELECT id FROM v_clientes_completo
           WHERE nombre = %s OR documento = %s
           LIMIT 1""",
        (nombre_o_documento, nombre_o_documento),
    )


def resolve_producto(nombre_o_codigo):
    if not nombre_o_codigo:
        return None
    return scalar(
        "SELECT PROD_ID FROM t_productos WHERE PROD_NOMBRE = %s OR PROD_CODIGO = %s LIMIT 1",
        (nombre_o_codigo, nombre_o_codigo),
    )


def ensure_cliente(nombre, documento=None):
    """Busca el cliente; si no existe lo crea junto con su persona."""
    cli_id = resolve_cliente(nombre or documento)
    if cli_id is not None:
        return cli_id

    per_id = None
    if documento:
        per_id = scalar("SELECT PER_ID FROM t_persona WHERE PER_IDENTIFICACION = %s LIMIT 1", (documento,))
    if per_id is None and nombre:
        per_id = scalar("SELECT PER_ID FROM t_persona WHERE PER_NOMBRE = %s LIMIT 1", (nombre,))

    if per_id is None:
        partes = (nombre or "Cliente sin nombre").split(None, 1)
        per_id = execute(
            """INSERT INTO t_persona (PER_UUID, PER_NOMBRE, PER_PRI_APELLIDO, PER_IDENTIFICACION, PER_CORREO)
               VALUES (%s, %s, %s, %s, %s)""",
            (new_uuid(), partes[0], partes[1] if len(partes) > 1 else "",
             unique_identificacion(documento), ""),
        )

    try:
        return execute(
            "INSERT INTO t_cliente (CLI_UUID, CLI_PER_ID) VALUES (%s, %s)",
            (new_uuid(), per_id),
        )
    except Exception:
        existente = scalar("SELECT CLI_ID FROM t_cliente WHERE CLI_PER_ID = %s LIMIT 1", (per_id,))
        if existente:
            return existente
        raise
