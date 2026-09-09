from flask import Flask
from config import Config
from Routes import load_routes
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config.from_object(Config)

mysql = MySQL(app)
app.mysql = mysql

@app.after_request
def add_cors_headers(response):
	response.headers["Access-Control-Allow-Origin"] = "*"
	response.headers["Access-Control-Allow-Headers"] = "Content-Type"
	response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
	return response

load_routes(app) 

 
# app.run(debug=True, port=5000, host='0.0.0.0')
