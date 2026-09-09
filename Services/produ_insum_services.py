from flask import current_app
from Models.produ_insum import Produ_insum
import uuid as uuid_lib

class produ_insum_services:
    def servListProduInsum():
        sql = "SELECT * FROM T_PRODU_INSUM"

        c   = current_app.mysql.connection.cursor() 
        c.execute(sql)
        
        data = c.fetchall()
        print(data)
        
        produ_insum_l =[ ]
        for u in data:
            produ_insum_l.append(Produ_insum(u[0],u[1],u[2],u[3],u[4]).to_dic())

        print(produ_insum_l)
        c.close()

        return produ_insum_l

    def addProduInsum(cantidad, producto_id, insumo_id):
        uuid = str(uuid_lib.uuid4())
        sql = "INSERT INTO T_PRODU_INSUM (PROINSU_UUID, PROINSU_CANTIDAD, PROINSU_PROD_ID, PROINSU_INS_ID) VALUES (%s, %s, %s, %s)"

        c   = current_app.mysql.connection.cursor()
        c.execute(sql, (uuid, cantidad, producto_id, insumo_id))
        current_app.mysql.connection.commit()

        c.close()
        return "Producto_Insumo agregado correctamente"

    def deleteProduInsum(id):
        sql = "DELETE FROM T_PRODU_INSUM WHERE PROINSU_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()
        c.close()

        return "Producto_Insumo eliminado correctamente"  

    def updateProduInsum(id, cantidad, producto_id, insumo_id):
        sql = "UPDATE T_PRODU_INSUM SET PROINSU_CANTIDAD = %s, PROINSU_PROD_ID = %s, PROINSU_INS_ID = %s WHERE PROINSU_ID = %s" 

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (cantidad, producto_id, insumo_id, id))
        current_app.mysql.connection.commit()
        c.close()

        return "Producto_Insumo actualizado correctamente"