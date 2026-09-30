from flask import current_app, request
from Models.vent_prod import Vent_prod
import uuid as uuid_lib

def servListVentProd():
    sql = "SELECT VENTPRO_ID, VENTPRO_UUID, VENTPRO_CANTIDAD, VENTPRO_VENT_ID, VENTPRO_PROD_ID FROM T_VENT_PROD"
    c = current_app.mysql.connection.cursor()
    c.execute(sql)
    data = c.fetchall()
    vent_prod_l = [Vent_prod(u[0],u[1],u[2],u[3],u[4]).to_dic() for u in data]
    c.close()
    return vent_prod_l

def addVentProd():
    data = request.get_json(silent=True) or {}
    uuid = str(uuid_lib.uuid4())
    sql = "INSERT INTO T_VENT_PROD (VENTPRO_UUID, VENTPRO_CANTIDAD, VENTPRO_VENT_ID, VENTPRO_PROD_ID) VALUES (%s, %s, %s, %s)"
    c = current_app.mysql.connection.cursor()
    c.execute(sql, (uuid, data.get("cantidad", 1), data.get("vent_id"), data.get("prod_id")))
    current_app.mysql.connection.commit()
    c.close()
    return {"mensaje": "Venta_producto agregado correctamente"}

def deleteVentProd(id):
    sql = "DELETE FROM T_VENT_PROD WHERE VENTPRO_ID = %s"
    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()
    c.close()
    return {"mensaje": "Venta_producto eliminado correctamente"}

def updateVentProd(id):
    data = request.get_json(silent=True) or {}
    uuid = str(uuid_lib.uuid4())
    sql = "UPDATE T_VENT_PROD SET VENTPRO_UUID = %s, VENTPRO_CANTIDAD = %s, VENTPRO_VENT_ID = %s, VENTPRO_PROD_ID = %s WHERE VENTPRO_ID = %s"
    c = current_app.mysql.connection.cursor()
    c.execute(sql, (uuid, data.get("cantidad", 1), data.get("vent_id"), data.get("prod_id"), id))
    current_app.mysql.connection.commit()
    c.close()
    return {"mensaje": "Venta_producto actualizado correctamente"}
