from flask import current_app
from Models.vent_prod import Vent_prod
import uuid as uuid_lib
from Services.validation import non_negative_number, positive_id, required_fields

def servListVentProd(id=None):
    sql = "SELECT VENTPRO_ID, VENTPRO_UUID, VENTPRO_CANTIDAD, VENTPRO_VENT_ID, VENTPRO_PROD_ID FROM T_VENT_PROD"
    if id is not None:
        sql += " WHERE VENTPRO_ID = %s"
    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,) if id is not None else ())
    data = c.fetchall()
    vent_prod_l = [Vent_prod(u[0],u[1],u[2],u[3],u[4]).to_dic() for u in data]
    c.close()
    return vent_prod_l

def addVentProd(data):
    if not isinstance(data, dict):
        return {"mensaje": "El cuerpo debe ser un objeto JSON"}, 400
    error = required_fields(data, ("vent_id", "prod_id"))
    if error:
        return error
    cantidad, error, status = non_negative_number(
        data.get("cantidad", 1), "cantidad", integer=True, strictly_positive=True
    )
    if error:
        return error, status
    vent_id, prod_id = positive_id(data.get("vent_id")), positive_id(data.get("prod_id"))
    if vent_id is None or prod_id is None:
        return {"mensaje": "Los IDs de venta y producto deben ser enteros positivos"}, 400
    uuid = str(uuid_lib.uuid4())
    sql = "INSERT INTO T_VENT_PROD (VENTPRO_UUID, VENTPRO_CANTIDAD, VENTPRO_VENT_ID, VENTPRO_PROD_ID) VALUES (%s, %s, %s, %s)"
    c = current_app.mysql.connection.cursor()
    c.execute("SELECT VENT_ID FROM T_VENTAS WHERE VENT_ID = %s", (vent_id,))
    if not c.fetchone():
        c.close()
        return {"mensaje": "Venta no encontrada"}, 404
    c.execute("SELECT PROD_ID FROM T_PRODUCTOS WHERE PROD_ID = %s", (prod_id,))
    if not c.fetchone():
        c.close()
        return {"mensaje": "Producto no encontrado"}, 404
    c.execute(sql, (uuid, cantidad, vent_id, prod_id))
    current_app.mysql.connection.commit()
    c.close()
    return {"mensaje": "Venta_producto agregado correctamente"}

def deleteVentProd(id):
    id = positive_id(id)
    if id is None:
        return {"mensaje": "El ID debe ser un entero positivo"}, 400
    sql = "DELETE FROM T_VENT_PROD WHERE VENTPRO_ID = %s"
    c = current_app.mysql.connection.cursor()
    c.execute("SELECT VENTPRO_ID FROM T_VENT_PROD WHERE VENTPRO_ID = %s", (id,))
    if not c.fetchone():
        c.close()
        return {"mensaje": "Detalle de venta no encontrado"}, 404
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()
    c.close()
    return {"mensaje": "Venta_producto eliminado correctamente"}

def updateVentProd(id, data):
    id = positive_id(id)
    if id is None:
        return {"mensaje": "El ID debe ser un entero positivo"}, 400
    if not isinstance(data, dict):
        return {"mensaje": "El cuerpo debe ser un objeto JSON"}, 400
    error = required_fields(data, ("vent_id", "prod_id"))
    if error:
        return error
    cantidad, error, status = non_negative_number(
        data.get("cantidad", 1), "cantidad", integer=True, strictly_positive=True
    )
    if error:
        return error, status
    vent_id, prod_id = positive_id(data.get("vent_id")), positive_id(data.get("prod_id"))
    if vent_id is None or prod_id is None:
        return {"mensaje": "Los IDs de venta y producto deben ser enteros positivos"}, 400
    uuid = str(uuid_lib.uuid4())
    sql = "UPDATE T_VENT_PROD SET VENTPRO_UUID = %s, VENTPRO_CANTIDAD = %s, VENTPRO_VENT_ID = %s, VENTPRO_PROD_ID = %s WHERE VENTPRO_ID = %s"
    c = current_app.mysql.connection.cursor()
    c.execute("SELECT VENTPRO_ID FROM T_VENT_PROD WHERE VENTPRO_ID = %s", (id,))
    if not c.fetchone():
        c.close()
        return {"mensaje": "Detalle de venta no encontrado"}, 404
    c.execute("SELECT VENT_ID FROM T_VENTAS WHERE VENT_ID = %s", (vent_id,))
    if not c.fetchone():
        c.close()
        return {"mensaje": "Venta no encontrada"}, 404
    c.execute("SELECT PROD_ID FROM T_PRODUCTOS WHERE PROD_ID = %s", (prod_id,))
    if not c.fetchone():
        c.close()
        return {"mensaje": "Producto no encontrado"}, 404
    c.execute(sql, (uuid, cantidad, vent_id, prod_id, id))
    current_app.mysql.connection.commit()
    c.close()
    return {"mensaje": "Venta_producto actualizado correctamente"}
