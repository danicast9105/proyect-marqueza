from flask import current_app
from Models.productos import Productos
import uuid as uuid_lib

def servListProductos():
    sql = "SELECT * FROM T_PRODUCTOS"

    c   = current_app.mysql.connection.cursor() 
    c.execute(sql)
    
    data = c.fetchall()
    print(data)
    
    productos_l =[ ]
    for u in data:
        productos_l.append(Productos(u[0],u[1],u[2],u[3],u[4],u[5],u[6],u[7],u[8]).to_dic())

    print(productos_l)
    c.close()

    return productos_l

def getProductos(id):
    c = current_app.mysql.connection.cursor()
    c.execute("SELECT * FROM T_PRODUCTOS WHERE PROD_ID = %s", (id,))
    row = c.fetchone()
    c.close()
    return Productos(*row).to_dic() if row else None

def addProductos(codigo, nombre, cantidad, precio, estado, usua_id, det_etc_id):
    sql = "INSERT INTO T_PRODUCTOS (PROD_UUID, PROD_CODIGO, PROD_NOMBRE, PROD_CANTIDAD, PROD_PRECIO, PROD_ESTADO, PROD_USUA_ID, PROD_DET_ETC_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    c   = current_app.mysql.connection.cursor()
    c.execute(sql, (str(uuid_lib.uuid4()), codigo, nombre, cantidad, precio, estado, usua_id, det_etc_id))
    current_app.mysql.connection.commit()

    c.close()
    return "Producto agregado correctamente"

def deleteProductos(id):
    sql = "DELETE FROM T_PRODUCTOS WHERE PROD_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()
    c.close()

    return "Producto eliminado correctamente"  

def updateProductos(id, codigo, nombre, cantidad, precio, estado, usua_id, det_etc_id):
    sql = "UPDATE T_PRODUCTOS SET PROD_CODIGO = %s, PROD_NOMBRE = %s, PROD_CANTIDAD = %s, PROD_PRECIO = %s, PROD_ESTADO = %s, PROD_USUA_ID = %s, PROD_DET_ETC_ID = %s WHERE PROD_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (codigo, nombre, cantidad, precio, estado, usua_id, det_etc_id, id))
    current_app.mysql.connection.commit()
    c.close()

    return "Producto actualizado correctamente"