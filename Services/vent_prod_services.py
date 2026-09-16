from flask import current_app
from Models.vent_prod import Vent_prod
import uuid as uuid_lib

def servListVentProd():
    c = current_app.mysql.connection.cursor()
    c.execute("SELECT * FROM T_VENT_PROD")
    data = c.fetchall()
    c.close()
    return [Vent_prod(*row).to_dic() for row in data]

def getVentProd(id):
    c = current_app.mysql.connection.cursor()
    c.execute("SELECT * FROM T_VENT_PROD WHERE VENTPRO_ID = %s", (id,))
    row = c.fetchone()
    c.close()
    return Vent_prod(*row).to_dic() if row else None

def addVentProd(cantidad, vent_id, prod_id):
    c = current_app.mysql.connection.cursor()
    c.execute("INSERT INTO T_VENT_PROD (VENTPRO_UUID, VENTPRO_CANTIDAD, VENTPRO_VENT_ID, VENTPRO_PROD_ID) VALUES (%s, %s, %s, %s)", (str(uuid_lib.uuid4()), cantidad, vent_id, prod_id))
    current_app.mysql.connection.commit()
    c.close()
    return "Venta_producto agregado correctamente"

def deleteVentProd(id):
    c = current_app.mysql.connection.cursor()
    c.execute("DELETE FROM T_VENT_PROD WHERE VENTPRO_ID = %s", (id,))
    current_app.mysql.connection.commit()
    c.close()
    return "Venta_producto eliminado correctamente"

def updateVentProd(id, cantidad, vent_id, prod_id):
    c = current_app.mysql.connection.cursor()
    c.execute("UPDATE T_VENT_PROD SET VENTPRO_CANTIDAD = %s, VENTPRO_VENT_ID = %s, VENTPRO_PROD_ID = %s WHERE VENTPRO_ID = %s", (cantidad, vent_id, prod_id, id))
    current_app.mysql.connection.commit()
    c.close()
    return "Venta_producto actualizado correctamente"