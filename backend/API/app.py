import os

from flask import Flask, g, jsonify, redirect, request, send_from_directory
from MySQLdb import Error as MySQLError

from config import Config
from flask_mysqldb import MySQL
from Routes import load_routes
from Services.auth_tokens import (
    InvalidAccessToken,
    TokenConfigurationError,
    ensure_access_token_table,
    is_access_token_active,
    verify_access_token,
)
from Services.usuarios_services import ensure_admin_user

app = Flask(__name__)
app.config.from_object(Config)
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
API_DOCS_HOST = os.getenv("API_DOCS_HOST", "api-marqueza.zona52.lat").strip().lower()

mysql = MySQL(app)
app.mysql = mysql


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        return "", 204


@app.before_request
def require_api_token():
    if request.endpoint is None or not request.path.startswith("/api/"):
        return None

    public_endpoints = {
        "health",
        "swagger_spec",
        "api_docs_alias",
        "auth_bp.login",
        "auth_bp.forgot_password",
        "auth_bp.reset_password",
    }
    if request.endpoint in public_endpoints:
        return None

    if not app.config.get("API_TOKEN_TABLE_READY"):
        try:
            ensure_access_token_table()
        except MySQLError:
            app.logger.exception("No se pudo preparar la tabla de tokens de acceso.")
            return jsonify({"message": "El servicio de autenticación no está disponible."}), 503

    authorization = request.headers.get("Authorization", "")
    scheme, separator, token = authorization.partition(" ")
    if not separator or scheme.lower() != "bearer" or not token.strip():
        return jsonify({"message": "Se requiere un token Bearer válido."}), 401

    try:
        user_token = verify_access_token(token.strip(), app.config.get("API_TOKEN_SECRET"))
    except TokenConfigurationError as error:
        app.logger.error("La autenticación de la API no está configurada: %s", error)
        return jsonify({"message": str(error)}), 503
    except InvalidAccessToken:
        return jsonify({"message": "El token de acceso es inválido o expiró."}), 401

    try:
        if not is_access_token_active(user_token["jti"]):
            return jsonify({"message": "El token de acceso fue revocado o la cuenta está desactivada."}), 401
    except MySQLError:
        app.logger.exception("No se pudo comprobar el estado del token de acceso.")
        return jsonify({"message": "No se pudo validar el token de acceso."}), 503

    g.api_user = user_token
    return None


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"message": "Recurso no encontrado"}), 404


@app.route("/")
def frontend_index():
    hostname = request.host.split(":", 1)[0].lower()
    if hostname == API_DOCS_HOST:
        return redirect("/documentacion")
    return redirect("/frontend/index.html")


@app.route("/frontend/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.errorhandler(405)
def method_not_allowed(_error):
    return jsonify({"message": "Metodo no permitido"}), 405


@app.errorhandler(500)
def internal_error(_error):
    current_app_mysql_rollback()
    return jsonify({"message": "Error interno del servidor"}), 500


def current_app_mysql_rollback():
    try:
        app.mysql.connection.rollback()
    except Exception:
        pass


@app.route("/api/health")
def health():
    try:
        c = app.mysql.connection.cursor()
        c.execute("SELECT 1")
        c.fetchone()
        c.close()
        database = "conectada"
    except Exception as error:
        database = f"error: {error}"
    return jsonify({"status": "ok", "database": database}), 200


@app.route("/documentacion")
def api_docs():
    return send_from_directory(
        os.path.join(os.path.dirname(__file__), "static", "swagger-ui"),
        "index.html",
    )


@app.route("/api/swagger.json")
def swagger_spec():
    return send_from_directory(
        os.path.dirname(__file__),
        "swagger.json",
        mimetype="application/json",
    )


@app.route("/api/docs")
@app.route("/api/docs/")
def api_docs_alias():
    return redirect("/documentacion")


load_routes(app)

with app.app_context():
    try:
        ensure_access_token_table()
        app.config["API_TOKEN_TABLE_READY"] = True
    except MySQLError:
        app.logger.exception("No se pudo preparar la tabla de tokens de acceso.")
        app.config["API_TOKEN_TABLE_READY"] = False

    try:
        ensure_admin_user()
    except Exception:
        app.logger.exception("No se pudo verificar o crear la cuenta principal de Administrador.")


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=True, port=port, host="0.0.0.0")
