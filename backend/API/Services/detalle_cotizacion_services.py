from flask import current_app, request
from Models.detalle_cotizacion import DetalleCotizacion
import uuid as uuid_lib

class detalle_cotizacion_services:
    def servListDetalleCotizacion():
        sql = "SELECT * FROM T_DETALLE_COTIZACION"
        c = current_app.mysql.connection.cursor()
        c.execute(sql)
        data = c.fetchall()
        detalles_l = [DetalleCotizacion(u[0],u[1],u[2],u[3],u[4],u[5],u[6],u[7],u[8]).to_dic() for u in data]
        c.close()
        return detalles_l

    def addDetalleCotizacion():
        data = request.get_json(silent=True) or {}
        uuid = str(uuid_lib.uuid4())
        sql = "INSERT INTO T_DETALLE_COTIZACION (DETCOT_UUID, DETCOT_COT_ID, DETCOT_PROD_ID, DETCOT_CODIGO, DETCOT_NOMBRE, DETCOT_CANTIDAD, DETCOT_PRECIO_UNITARIO, DETCOT_SUBTOTAL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        c = current_app.mysql.connection.cursor()
        c.execute(sql, (uuid, data.get("cot_id"), data.get("prod_id"), data.get("codigo",""), data.get("nombre",""), data.get("cantidad",1), data.get("precio_unitario",0.00), data.get("subtotal",0.00)))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Detalle de cotización agregado correctamente"}

    def deleteDetalleCotizacion(id):
        sql = "DELETE FROM T_DETALLE_COTIZACION WHERE DETCOT_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Detalle de cotización eliminado correctamente"}

    def updateDetalleCotizacion(id):
        data = request.get_json(silent=True) or {}
        uuid = str(uuid_lib.uuid4())
        sql = "UPDATE T_DETALLE_COTIZACION SET DETCOT_UUID = %s, DETCOT_COT_ID = %s, DETCOT_PROD_ID = %s, DETCOT_CODIGO = %s, DETCOT_NOMBRE = %s, DETCOT_CANTIDAD = %s, DETCOT_PRECIO_UNITARIO = %s, DETCOT_SUBTOTAL = %s WHERE DETCOT_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute(sql, (uuid, data.get("cot_id"), data.get("prod_id"), data.get("codigo",""), data.get("nombre",""), data.get("cantidad",1), data.get("precio_unitario",0.00), data.get("subtotal",0.00), id))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Detalle de cotización actualizado correctamente"}
