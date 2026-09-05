from flask import current_app
from Models.etc import ETC
import uuid as uuid_lib

class etc_services:
    def servListETC():
        sql = "SELECT * FROM T_ESTADO_TIPOS_CATEGORIAS"

        c   = current_app.mysql.connection.cursor() 
        c.execute(sql)
        
        data = c.fetchall()
        print(data)
        
        etc_l =[ ]
        for u in data:
            etc_l.append(ETC(u[0],u[1],u[2]).to_dic())

        print(etc_l)
        c.close()

        return etc_l

    def addETC(etc_nombre):
        uuid = str(uuid_lib.uuid4())
        sql = "INSERT INTO T_ESTADO_TIPOS_CATEGORIAS (ETC_UUID, ETC_NOMBRE) VALUES (%s, %s)"

        c   = current_app.mysql.connection.cursor()
        c.execute(sql, (uuid, etc_nombre))
        current_app.mysql.connection.commit()

        c.close()
        return "ETC agregado correctamente"

    def deleteETC(id):
        sql = "DELETE FROM T_ESTADO_TIPOS_CATEGORIAS WHERE ETC_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()
        c.close()

        return "ETC eliminado correctamente"  

    def updateETC(id, etc_nombre):
        sql = "UPDATE T_ESTADO_TIPOS_CATEGORIAS SET ETC_NOMBRE = %s WHERE ETC_ID = %s" 

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (etc_nombre, id))
        current_app.mysql.connection.commit()
        c.close()

        return "ETC actualizado correctamente"