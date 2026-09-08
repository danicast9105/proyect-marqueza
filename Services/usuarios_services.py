from flask import current_app
from Models.usuarios import Usuarios
import uuid as uuid_lib

def servListUsuarios():
    sql = "SELECT * FROM T_USUARIOS"

    c   = current_app.mysql.connection.cursor() 
    c.execute(sql)
    
    data = c.fetchall()
    print(data)
    
    usuarios_l =[ ]
    for u in data:
        usuarios_l.append(Usuarios(u[0],u[1],u[2],u[3],u[4],u[5],u[6]).to_dic())

    print(usuarios_l)
    c.close()

    return usuarios_l

def addUsuarios(nombre, correo, contrasena, estado, det_etc_id):
    c   = current_app.mysql.connection.cursor()
    c.execute("SELECT COALESCE(MAX(USUA_ID), 0) + 1 FROM T_USUARIOS")
    next_id = c.fetchone()[0]

    sql = "INSERT INTO T_USUARIOS (USUA_ID, USUA_UUID, USUA_NOMBRE, USUA_CORREO, USUA_CONTRASEÑA, USUA_ESTADO, USUA_DET_ETC_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    c.execute(sql, (next_id, str(uuid_lib.uuid4()), nombre, correo, contrasena, estado, det_etc_id))
    current_app.mysql.connection.commit()

    c.close()
    return {"mensaje": "Usuario agregado correctamente", "id": next_id}

def deleteUsuarios(id):
    sql = "DELETE FROM T_USUARIOS WHERE USUA_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()
    c.close()

    return "Usuario eliminado correctamente"

def updateUsuarios(id, nombre, correo, contrasena, estado, det_etc_id):
    sql = "UPDATE T_USUARIOS SET USUA_NOMBRE = %s, USUA_CORREO = %s, USUA_CONTRASEÑA = %s, USUA_ESTADO = %s, USUA_DET_ETC_ID = %s WHERE USUA_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (nombre, correo, contrasena, estado, det_etc_id, id))
    current_app.mysql.connection.commit()
    c.close()

    return "Usuario actualizado correctamente"