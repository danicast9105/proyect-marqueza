from flask import current_app
from Models.ventas import Ventas
import uuid as uuid_lib

def servListVentas():
    c = current_app.mysql.connection.cursor()
    c.execute("SELECT * FROM T_VENTAS")
    data = c.fetchall()
    c.close()
    return [Ventas(*row).to_dic() for row in data]

def getVentas(id):
    c = current_app.mysql.connection.cursor()
    c.execute("SELECT * FROM T_VENTAS WHERE VENT_ID = %s", (id,))
    row = c.fetchone()
    c.close()
    return Ventas(*row).to_dic() if row else None

def addVentas(fecha, usua_id, cli_id):
    c = current_app.mysql.connection.cursor()
    c.execute("INSERT INTO T_VENTAS (VENT_UUID, VENT_FECHA, VENT_USUA_ID, VENT_CLI_ID) VALUES (%s, %s, %s, %s)", (str(uuid_lib.uuid4()), fecha, usua_id, cli_id))
    current_app.mysql.connection.commit()
    c.close()
    return "Venta agregado correctamente"

def deleteVentas(id):
    c = current_app.mysql.connection.cursor()
    c.execute("DELETE FROM T_VENTAS WHERE VENT_ID = %s", (id,))
    current_app.mysql.connection.commit()
    c.close()
    return "Venta eliminado correctamente"

def updateVentas(id, fecha, usua_id, cli_id):
    c = current_app.mysql.connection.cursor()
    c.execute("UPDATE T_VENTAS SET VENT_FECHA = %s, VENT_USUA_ID = %s, VENT_CLI_ID = %s WHERE VENT_ID = %s", (fecha, usua_id, cli_id, id))
    current_app.mysql.connection.commit()
    c.close()
    return "Venta actualizado correctamente"