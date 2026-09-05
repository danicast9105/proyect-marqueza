from flask import current_app
from Models.proveedor import Proveedor

def servListProveedor():
    sql = "SELECT * FROM T_PROVEEDORES"

    c   = current_app.mysql.connection.cursor() 
    c.execute(sql)
    
    data = c.fetchall()
    print(data)
    
    proveedores_l =[ ]
    for u in data:
        proveedores_l.append(Proveedor(u[0],u[1],u[2]).to_dic())

    print(proveedores_l)
    c.close()

    return proveedores_l

def addProveedor():
    sql = "INSERT INTO T_PROVEEDORES (PROV_UUID, PROV_PER_ID) VALUES (%s, %s)"

    c   = current_app.mysql.connection.cursor()
    c.execute(sql, ("prov_uuid", "prov_per_id"))
    current_app.mysql.connection.commit()

    c.close()
    return "Proveedor agregado correctamente"

def deleteProveedor():
    sql = "DELETE FROM T_PROVEEDORES WHERE PROV_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("prov_id",))
    current_app.mysql.connection.commit()
    c.close()

    return "Proveedor eliminado correctamente"

def updateProveedor():
    sql = "UPDATE T_PROVEEDORES SET PROV_UUID = %s, PROV_PER_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("prov_uuid", "prov_per_id"))
    current_app.mysql.connection.commit()
    c.close()

    return "Proveedor actualizado correctamente"