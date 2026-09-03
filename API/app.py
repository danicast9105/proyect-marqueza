from flask import Flask
from config import Config
from Routes import load_routes
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config.from_object(Config)

mysql = MySQL(app)
app.mysql = mysql

load_routes(app) 

 
app.run(debug=True, port=5000, host='0.0.0.0')