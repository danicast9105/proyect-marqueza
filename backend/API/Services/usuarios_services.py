from flask import current_app
from Models.usuarios import Usuarios

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

def addUsuarios():
    sql = "INSERT INTO T_USUARIOS (USUA_UUID, USUA_NOMBRE, USUA_CORREO, USUA_CONTRASEÑA, USUA_ESTADO, USUA_DET_ETC_ID) VALUES (%s, %s, %s, %s, %s, %s)"

    c   = current_app.mysql.connection.cursor()
    c.execute(sql, ("usua_uuid, usua_nombre, usua_correo, usua_contraseña, usua_estado, usua_det_etc_id"))
    current_app.mysql.connection.commit()

    c.close()
    return "Usuario agregado correctamente"

def deleteUsuarios():
    sql = "DELETE FROM T_USUARIOS WHERE USUA_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("usua_id",))
    current_app.mysql.connection.commit()
    c.close()

    return "Usuario eliminado correctamente"

def updateUsuarios():
    sql = "UPDATE T_USUARIOS SET USUA_UUID = %s, USUA_NOMBRE = %s, USUA_CORREO = %s, USUA_CONTRASEÑA = %s, USUA_ESTADO = %s, USUA_DET_ETC_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("usua_uuid, usua_nombre, usua_correo, usua_contraseña, usua_estado, usua_det_etc_id"))
    current_app.mysql.connection.commit()
    c.close()

    return "Usuario actualizado correctamente"