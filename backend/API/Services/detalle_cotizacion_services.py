from flask import current_app
from Models.detalle_cotizacion import DetalleCotizacion
import uuid as uuid_lib
from Services.validation import non_negative_number, positive_id, required_fields

class detalle_cotizacion_services:
    def servListDetalleCotizacion(id=None):
        sql = "SELECT * FROM T_DETALLE_COTIZACION"
        if id is not None:
            sql += " WHERE DETCOT_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,) if id is not None else ())
        data = c.fetchall()
        detalles_l = [DetalleCotizacion(u[0],u[1],u[2],u[3],u[4],u[5],u[6],u[7],u[8]).to_dic() for u in data]
        c.close()
        return detalles_l

    def addDetalleCotizacion(data):
        if not isinstance(data, dict):
            return {"mensaje": "El cuerpo debe ser un objeto JSON"}, 400
        error = required_fields(data, ("cot_id", "nombre"))
        if error:
            return error
        cot_id = positive_id(data.get("cot_id"))
        if cot_id is None:
            return {"mensaje": "El ID de cotizacion debe ser un entero positivo"}, 400
        prod_id = data.get("prod_id")
        if prod_id not in (None, ""):
            prod_id = positive_id(prod_id)
            if prod_id is None:
                return {"mensaje": "El ID de producto debe ser un entero positivo"}, 400
        cantidad, error, status = non_negative_number(
            data.get("cantidad", 1), "cantidad", integer=True, strictly_positive=True
        )
        if error:
            return error, status
        for field in ("precio_unitario", "subtotal"):
            _, error, status = non_negative_number(data.get(field, 0), field)
            if error:
                return error, status
        uuid = str(uuid_lib.uuid4())
        sql = "INSERT INTO T_DETALLE_COTIZACION (DETCOT_UUID, DETCOT_COT_ID, DETCOT_PROD_ID, DETCOT_CODIGO, DETCOT_NOMBRE, DETCOT_CANTIDAD, DETCOT_PRECIO_UNITARIO, DETCOT_SUBTOTAL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        c = current_app.mysql.connection.cursor()
        c.execute("SELECT COT_ID FROM T_COTIZACIONES WHERE COT_ID = %s", (cot_id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Cotizacion no encontrada"}, 404
        if prod_id is not None:
            c.execute("SELECT PROD_ID FROM T_PRODUCTOS WHERE PROD_ID = %s", (prod_id,))
            if not c.fetchone():
                c.close()
                return {"mensaje": "Producto no encontrado"}, 404
        c.execute(sql, (uuid, cot_id, prod_id, data.get("codigo",""), data.get("nombre",""), cantidad, data.get("precio_unitario",0.00), data.get("subtotal",0.00)))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Detalle de cotización agregado correctamente"}

    def deleteDetalleCotizacion(id):
        id = positive_id(id)
        if id is None:
            return {"mensaje": "El ID debe ser un entero positivo"}, 400
        sql = "DELETE FROM T_DETALLE_COTIZACION WHERE DETCOT_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute("SELECT DETCOT_ID FROM T_DETALLE_COTIZACION WHERE DETCOT_ID = %s", (id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Detalle de cotizacion no encontrado"}, 404
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Detalle de cotización eliminado correctamente"}

    def updateDetalleCotizacion(id, data):
        id = positive_id(id)
        if id is None:
            return {"mensaje": "El ID debe ser un entero positivo"}, 400
        if not isinstance(data, dict):
            return {"mensaje": "El cuerpo debe ser un objeto JSON"}, 400
        error = required_fields(data, ("cot_id", "nombre"))
        if error:
            return error
        cot_id = positive_id(data.get("cot_id"))
        if cot_id is None:
            return {"mensaje": "El ID de cotizacion debe ser un entero positivo"}, 400
        prod_id = data.get("prod_id")
        if prod_id not in (None, ""):
            prod_id = positive_id(prod_id)
            if prod_id is None:
                return {"mensaje": "El ID de producto debe ser un entero positivo"}, 400
        cantidad, error, status = non_negative_number(
            data.get("cantidad", 1), "cantidad", integer=True, strictly_positive=True
        )
        if error:
            return error, status
        for field in ("precio_unitario", "subtotal"):
            _, error, status = non_negative_number(data.get(field, 0), field)
            if error:
                return error, status
        uuid = str(uuid_lib.uuid4())
        sql = "UPDATE T_DETALLE_COTIZACION SET DETCOT_UUID = %s, DETCOT_COT_ID = %s, DETCOT_PROD_ID = %s, DETCOT_CODIGO = %s, DETCOT_NOMBRE = %s, DETCOT_CANTIDAD = %s, DETCOT_PRECIO_UNITARIO = %s, DETCOT_SUBTOTAL = %s WHERE DETCOT_ID = %s"
        c = current_app.mysql.connection.cursor()
        c.execute("SELECT DETCOT_ID FROM T_DETALLE_COTIZACION WHERE DETCOT_ID = %s", (id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Detalle de cotizacion no encontrado"}, 404
        c.execute("SELECT COT_ID FROM T_COTIZACIONES WHERE COT_ID = %s", (cot_id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Cotizacion no encontrada"}, 404
        if prod_id is not None:
            c.execute("SELECT PROD_ID FROM T_PRODUCTOS WHERE PROD_ID = %s", (prod_id,))
            if not c.fetchone():
                c.close()
                return {"mensaje": "Producto no encontrado"}, 404
        c.execute(sql, (uuid, cot_id, prod_id, data.get("codigo",""), data.get("nombre",""), cantidad, data.get("precio_unitario",0.00), data.get("subtotal",0.00), id))
        current_app.mysql.connection.commit()
        c.close()
        return {"mensaje": "Detalle de cotización actualizado correctamente"}
