from flask import current_app
from Models.cotizaciones import Cotizaciones
import uuid as uuid_lib

class cotizaciones_services:
    def servListCotizaciones():
        sql = "SELECT * FROM T_COTIZACIONES"

        c   = current_app.mysql.connection.cursor() 
        c.execute(sql)
        
        data = c.fetchall()
        print(data)
        
        cotizaciones_l =[ ]
        for u in data:
            cotizaciones_l.append(Cotizaciones(u[0],u[1],u[2],u[3],u[4],u[5],u[6],u[7],u[8]).to_dic())

        print(cotizaciones_l)
        c.close()

        return cotizaciones_l

    def addCotizaciones(pro_codigo, pro_nombre, pro_cantidad, pro_precio, total_pagar, usuario_id, cliente_id):
        uuid = str(uuid_lib.uuid4())
        sql = "INSERT INTO T_COTIZACIONES (COT_UUID, COT_PRO_CODIGO, COT_PRO_NOMBRE, COT_PRO_CANTIDAD, COT_PRO_PRECIO, COT_TOTAL_PAGAR, COT_USUA_ID, COT_CLI_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        c   = current_app.mysql.connection.cursor()
        c.execute(sql, (uuid, pro_codigo, pro_nombre, pro_cantidad, pro_precio, total_pagar, usuario_id, cliente_id))
        current_app.mysql.connection.commit()

        c.close()
        return "Cotización agregada correctamente"

    def deleteCotizaciones(id):
        sql = "DELETE FROM T_COTIZACIONES WHERE COT_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()
        c.close()

        return "Cotización eliminada correctamente"

    def updateCotizaciones(id, pro_codigo, pro_nombre, pro_cantidad, pro_precio, total_pagar, usuario_id, cliente_id):
        sql = "UPDATE T_COTIZACIONES SET COT_PRO_CODIGO = %s, COT_PRO_NOMBRE = %s, COT_PRO_CANTIDAD = %s, COT_PRO_PRECIO = %s, COT_TOTAL_PAGAR = %s, COT_USUA_ID = %s, COT_CLI_ID = %s WHERE COT_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (pro_codigo, pro_nombre, pro_cantidad, pro_precio, total_pagar, usuario_id, cliente_id, id))
        current_app.mysql.connection.commit()
        c.close()

        return "Cotización actualizada correctamente"