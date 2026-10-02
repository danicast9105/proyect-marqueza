import os

from flask import Flask, jsonify, redirect, request, send_from_directory

from config import Config
from flask_mysqldb import MySQL
from Routes import load_routes
from Services.usuarios_services import ensure_admin_user

app = Flask(__name__)
app.config.from_object(Config)
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))

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


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"message": "Recurso no encontrado"}), 404


@app.route("/")
def frontend_index():
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


load_routes(app)

with app.app_context():
    try:
        ensure_admin_user()
    except Exception:
        app.logger.exception("No se pudo verificar o crear la cuenta principal de Administrador.")


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=True, port=port, host="0.0.0.0")
