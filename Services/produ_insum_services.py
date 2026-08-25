from flask import current_app
from Models.produ_insum import Produ_insum

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

def addProduInsum():
    sql = "INSERT INTO T_PRODU_INSUM (PRODINSU_UUID, PRODINSU_CANTIDAD, PRODINSU_PROD_ID, PRODINSU_INS_ID) VALUES (%s, %s, %s, %s)"

    c   = current_app.mysql.connection.cursor()
    c.execute(sql, ("prodinsu_uuid", "prodinsu_cantidad, prodinsu_prod_id, prodinsu_ins_id"))
    current_app.mysql.connection.commit()

    c.close()
    return "Producto_Insumo agregado correctamente"

def deleteProduInsum():
    sql = "DELETE FROM T_PRODU_INSUM WHERE PRODINSU_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("prodinsu_id",))
    current_app.mysql.connection.commit()
    c.close()

    return "Producto_Insumo eliminado correctamente"  

def updateProduInsum():
    sql = "UPDATE T_PRODU_INSUM SET PRODINSU_UUID = %s, PRODINSU_CANTIDAD = %s, PRODINSU_PROD_ID = %s, PRODINSU_INS_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("prodinsu_uuid", "prodinsu_cantidad, prodinsu_prod_id, prodinsu_ins_id"))
    current_app.mysql.connection.commit()
    c.close()

    return "Producto_Insumo actualizado correctamente"