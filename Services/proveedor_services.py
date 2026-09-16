from flask import current_app
from Models.proveedor import Proveedor
import uuid as uuid_lib

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

def getProveedor(id):
    c = current_app.mysql.connection.cursor()
    c.execute("SELECT * FROM T_PROVEEDORES WHERE PROV_ID = %s", (id,))
    row = c.fetchone()
    c.close()
    return Proveedor(*row).to_dic() if row else None

def addProveedor(per_id):
    sql = "INSERT INTO T_PROVEEDORES (PROV_UUID, PROV_PER_ID) VALUES (%s, %s)"

    c   = current_app.mysql.connection.cursor()
    c.execute(sql, (str(uuid_lib.uuid4()), per_id))
    current_app.mysql.connection.commit()

    c.close()
    return "Proveedor agregado correctamente"

def deleteProveedor(id):
    sql = "DELETE FROM T_PROVEEDORES WHERE PROV_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()
    c.close()

    return "Proveedor eliminado correctamente"

def updateProveedor(id, per_id):
    sql = "UPDATE T_PROVEEDORES SET PROV_PER_ID = %s WHERE PROV_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (per_id, id))
    current_app.mysql.connection.commit()
    c.close()

    return "Proveedor actualizado correctamente"