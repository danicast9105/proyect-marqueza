from flask import current_app
from Models.vent_prod import Vent_prod

def servListVentProd():
    sql = "SELECT * FROM T_VENT_PROD"

    c   = current_app.mysql.connection.cursor() 
    c.execute(sql)
    
    data = c.fetchall()
    print(data)
    
    vent_prod_l =[ ]
    for u in data:
        vent_prod_l.append(Vent_prod(u[0],u[1],u[2],u[3],u[4]).to_dic())

    print(vent_prod_l)
    c.close()

    return vent_prod_l

def addVentProd():
    sql = "INSERT INTO T_VENT_PROD (VENTPRO_UUID, VENTPRO_CANTIDAD, VENTPRO_VENT_ID, VENTPRO_PROD_ID) VALUES (%s, %s, %s, %s)"

    c   = current_app.mysql.connection.cursor()
    c.execute(sql, ("ventpro_uuid, ventpro_cantidad, ventpro_vent_id, ventpro_prod_id"))
    current_app.mysql.connection.commit()

    c.close()
    return "Venta_producto agregado correctamente"

def deleteVentProd():
    sql = "DELETE FROM T_VENT_PROD WHERE VENTPRO_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("ventpro_id",))
    current_app.mysql.connection.commit()
    c.close()

    return "Usuario eliminado correctamente"

def updateVentProd():
    sql = "UPDATE T_VENT_PROD SET VENTPRO_UUID = %s, VENTPRO_CANTIDAD = %s, VENTPRO_VENT_ID = %s, VENTPRO_PROD_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("ventpro_uuid, ventpro_cantidad, ventpro_vent_id, ventpro_prod_id"))
    current_app.mysql.connection.commit()
    c.close()

    return "Venta_producto actualizado correctamente"