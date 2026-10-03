import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST") or os.getenv("mysql_host")
    MYSQL_USER = os.getenv("MYSQL_USER") or os.getenv("mysql_user")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD") or os.getenv("mysql_password")
    MYSQL_DB = os.getenv("MYSQL_DB") or os.getenv("MYSQL_DATABASE") or os.getenv("mysql_db")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT") or os.getenv("mysql_port") or "3306")
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "false").lower() == "true"
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_FROM = os.getenv("SMTP_FROM")
    SMTP_TIMEOUT = int(os.getenv("SMTP_TIMEOUT", "15"))
    FRONTEND_RESET_URL = os.getenv(
        "FRONTEND_RESET_URL",
        "http://localhost:5000/frontend/olvido_contrasena/restablecer.html",
    )
