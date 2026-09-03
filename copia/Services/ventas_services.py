from flask import current_app
from Models.ventas import Ventas

def servListVentas():
    sql = "SELECT * FROM T_VENTAS"

    c   = current_app.mysql.connection.cursor() 
    c.execute(sql)
    
    data = c.fetchall()
    print(data)
    
    ventas_l =[ ]
    for u in data:
        ventas_l.append(Ventas(u[0],u[1],u[2],u[3],u[4],u[5]).to_dic())

    print(ventas_l)
    c.close()

    return ventas_l

def addVentas():
    sql = "INSERT INTO T_VENTAS (VENT_UUID, VENT_FECHA, VENT_USUA_ID, VENT_CLI_ID) VALUES (%s, %s, %s, %s)"

    c   = current_app.mysql.connection.cursor()
    c.execute(sql, ("vent_uuid, vent_fecha, vent_usua_id, vent_cli_id"))
    current_app.mysql.connection.commit()

    c.close()
    return "Venta agregado correctamente"

def deleteVentas():
    sql = "DELETE FROM T_VENTAS WHERE VENT_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("vent_id",))
    current_app.mysql.connection.commit()
    c.close()

    return "Venta eliminado correctamente"

def updateVentas():
    sql = "UPDATE T_VENTAS SET VENT_UUID = %s, VENT_FECHA = %s, VENT_USUA_ID = %s, VENT_CLI_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("vent_uuid, vent_fecha, vent_usua_id, vent_cli_id"))
    current_app.mysql.connection.commit()
    c.close()

    return "Venta actualizado correctamente"