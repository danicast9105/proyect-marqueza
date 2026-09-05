from flask import current_app
from Models.etc import ETC

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

def addETC():
    sql = "INSERT INTO T_ESTADO_TIPOS_CATEGORIAS (ETC_UUID, ETC_NOMBRE) VALUES (%s, %s)"

    c   = current_app.mysql.connection.cursor()
    c.execute(sql, ("etc_uuid", "etc_nombre"))
    current_app.mysql.connection.commit()

    c.close()
    return "ETC agregado correctamente"

def deleteETC():
    sql = "DELETE FROM T_ESTADO_TIPOS_CATEGORIAS WHERE ETC_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("etc_id",))
    current_app.mysql.connection.commit()
    c.close()

    return "ETC eliminado correctamente"  

def updateETC():
    sql = "UPDATE T_ESTADO_TIPOS_CATEGORIAS SET ETC_UUID = %s, ETC_NOMBRE = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("etc_uuid", "etc_nombre"))
    current_app.mysql.connection.commit()
    c.close()

    return "ETC actualizado correctamente"