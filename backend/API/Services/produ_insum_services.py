from flask import current_app
from Models.produ_insum import Produ_insum
import uuid as uuid_lib
from Services.validation import non_negative_number, positive_id, required_fields

class produ_insum_services:
    def servListProduInsum(id=None):
        sql = "SELECT PROINSU_ID, PROINSU_UUID, PROINSU_CANTIDAD, PROINSU_PROD_ID, PROINSU_INS_ID FROM T_PRODU_INSUM"
        if id is not None:
            sql += " WHERE PROINSU_ID = %s"

        c   = current_app.mysql.connection.cursor() 
        c.execute(sql, (id,) if id is not None else ())
        
        data = c.fetchall()
        print(data)
        
        produ_insum_l =[ ]
        for u in data:
            produ_insum_l.append(Produ_insum(u[0],u[1],u[2],u[3],u[4]).to_dic())

        print(produ_insum_l)
        c.close()

        return produ_insum_l

    def addProduInsum(cantidad, producto_id, insumo_id):
        error = required_fields(
            {"cantidad": cantidad, "producto_id": producto_id, "insumo_id": insumo_id},
            ("cantidad", "producto_id", "insumo_id"),
        )
        if error:
            return error
        cantidad, error, status = non_negative_number(
            cantidad, "cantidad", strictly_positive=True
        )
        if error:
            return error, status
        producto_id, insumo_id = positive_id(producto_id), positive_id(insumo_id)
        if producto_id is None or insumo_id is None:
            return {"mensaje": "Los IDs de producto e insumo deben ser enteros positivos"}, 400
        uuid = str(uuid_lib.uuid4())
        sql = "INSERT INTO T_PRODU_INSUM (PROINSU_UUID, PROINSU_CANTIDAD, PROINSU_PROD_ID, PROINSU_INS_ID) VALUES (%s, %s, %s, %s)"

        c   = current_app.mysql.connection.cursor()
        c.execute("SELECT PROD_ID FROM T_PRODUCTOS WHERE PROD_ID = %s", (producto_id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Producto no encontrado"}, 404
        c.execute("SELECT INS_ID FROM T_INSUMOS WHERE INS_ID = %s", (insumo_id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Insumo no encontrado"}, 404
        c.execute(
            "SELECT PROINSU_ID FROM T_PRODU_INSUM WHERE PROINSU_PROD_ID = %s AND PROINSU_INS_ID = %s",
            (producto_id, insumo_id),
        )
        if c.fetchone():
            c.close()
            return {"mensaje": "La relacion producto-insumo ya existe"}, 409
        c.execute(sql, (uuid, cantidad, producto_id, insumo_id))
        current_app.mysql.connection.commit()

        c.close()
        return "Producto_Insumo agregado correctamente"

    def deleteProduInsum(id):
        id = positive_id(id)
        if id is None:
            return {"mensaje": "El ID debe ser un entero positivo"}, 400
        sql = "DELETE FROM T_PRODU_INSUM WHERE PROINSU_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute("SELECT PROINSU_ID FROM T_PRODU_INSUM WHERE PROINSU_ID = %s", (id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Relacion producto-insumo no encontrada"}, 404
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()
        c.close()

        return "Producto_Insumo eliminado correctamente"  

    def updateProduInsum(id, cantidad, producto_id, insumo_id):
        id = positive_id(id)
        if id is None:
            return {"mensaje": "El ID debe ser un entero positivo"}, 400
        error = required_fields(
            {"cantidad": cantidad, "producto_id": producto_id, "insumo_id": insumo_id},
            ("cantidad", "producto_id", "insumo_id"),
        )
        if error:
            return error
        cantidad, error, status = non_negative_number(
            cantidad, "cantidad", strictly_positive=True
        )
        if error:
            return error, status
        producto_id, insumo_id = positive_id(producto_id), positive_id(insumo_id)
        if producto_id is None or insumo_id is None:
            return {"mensaje": "Los IDs de producto e insumo deben ser enteros positivos"}, 400
        sql = "UPDATE T_PRODU_INSUM SET PROINSU_CANTIDAD = %s, PROINSU_PROD_ID = %s, PROINSU_INS_ID = %s WHERE PROINSU_ID = %s" 

        c = current_app.mysql.connection.cursor()
        c.execute("SELECT PROINSU_ID FROM T_PRODU_INSUM WHERE PROINSU_ID = %s", (id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Relacion producto-insumo no encontrada"}, 404
        c.execute("SELECT PROD_ID FROM T_PRODUCTOS WHERE PROD_ID = %s", (producto_id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Producto no encontrado"}, 404
        c.execute("SELECT INS_ID FROM T_INSUMOS WHERE INS_ID = %s", (insumo_id,))
        if not c.fetchone():
            c.close()
            return {"mensaje": "Insumo no encontrado"}, 404
        c.execute(
            """SELECT PROINSU_ID FROM T_PRODU_INSUM
               WHERE PROINSU_PROD_ID = %s AND PROINSU_INS_ID = %s AND PROINSU_ID <> %s""",
            (producto_id, insumo_id, id),
        )
        if c.fetchone():
            c.close()
            return {"mensaje": "La relacion producto-insumo ya existe"}, 409
        c.execute(sql, (cantidad, producto_id, insumo_id, id))
        current_app.mysql.connection.commit()
        c.close()

        return "Producto_Insumo actualizado correctamente"