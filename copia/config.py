import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST") or os.getenv("mysql_host")
    MYSQL_USER = os.getenv("MYSQL_USER") or os.getenv("mysql_user")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD") or os.getenv("mysql_password")
    MYSQL_DB = os.getenv("MYSQL_DB") or os.getenv("MYSQL_DATABASE") or os.getenv("mysql_db")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT") or os.getenv("mysql_port"))
