from flask import current_app
from Models.detalles_etc import Detalles_etc

def servListDetalles_etc():
    sql = "SELECT * FROM T_DETALLES_ETC"

    c   = current_app.mysql.connection.cursor() 
    c.execute(sql)
    
    data = c.fetchall()
    print(data)
    
    detalles_etc_l =[ ]
    for u in data:
        detalles_etc_l.append(Detalles_etc(u[0],u[1],u[2],u[3],u[4]).to_dic())

    print(detalles_etc_l)
    c.close()

    return detalles_etc_l

def addDetalles_etc():
    sql = "INSERT INTO T_DETALLES_ETC (DET_ETC_UUID, DET_ETC_NOMBRE, DET_ETC_ETC_ID, DET_ETC_PER_ID) VALUES (%s, %s, %s, %s)"

    c   = current_app.mysql.connection.cursor()
    c.execute(sql, ("det_etc_uuid", "det_etc_nombre", "det_etc_etc_id", "det_etc_per_id"))
    current_app.mysql.connection.commit()

    c.close()
    return "Detalle agregado correctamente"

def deleteDetalles_etc():
    sql = "DELETE FROM T_DETALLES_ETC WHERE DET_ETC_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("det_etc_id",))
    current_app.mysql.connection.commit()
    c.close()

    return "Detalle eliminado correctamente"  

def updateDetalles_etc():
    sql = "UPDATE T_DETALLES_ETC SET DET_ETC_NOMBRE = %s, DET_ETC_ETC_ID = %s, DET_ETC_PER_ID = %s WHERE DET_ETC_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("det_etc_nombre", "det_etc_etc_id", "det_etc_per_id", "det_etc_id"))
    current_app.mysql.connection.commit()
    c.close()

    return "Detalle actualizado correctamente"