from flask import current_app
from Models.persona import Persona
from uuid import uuid4

def servListPersona():
    sql = "SELECT * FROM T_PERSONA"

    c   = current_app.mysql.connection.cursor() 
    c.execute(sql)
    
    data = c.fetchall()
    print(data)
    
    personas_l =[ ]
    for u in data:
        personas_l.append(Persona(u[0],u[1],u[2],u[3],u[4],u[5],u[6],u[7],u[8],u[9]).to_dic())

    print(personas_l)
    c.close()

    return personas_l

def addPersona(p_nombre, s_nombre, p_apellido, s_apellido, correo, direccion, identificacion, telefono):

    uuid = str(uuid4())
    sql = "INSERT INTO T_PERSONA (PER_UUID, PER_NOMBRE, PER_SEG_NOMBRE, PER_PRI_APELLIDO, PER_SEG_APELLIDO, PER_CORREO, PER_DIRECCION, PER_IDENTIFICACION, PER_TELEFONO) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    c   = current_app.mysql.connection.cursor()
    c.execute(sql, (uuid, p_nombre, s_nombre, p_apellido, s_apellido, correo, direccion, identificacion, telefono))
    current_app.mysql.connection.commit()

    c.close()
    return "Persona agregada correctamente"

def deletePersona(id):
    sql = "DELETE FROM T_PERSONA WHERE PER_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, (id,))
    current_app.mysql.connection.commit()
    c.close()

    return "Persona eliminada correctamente"

def updatePersona():
    sql = "UPDATE T_PERSONA SET PER_NOMBRE = %s, PER_SEG_NOMBRE = %s, PER_PRI_APELLIDO = %s, PER_SEG_APELLIDO = %s, PER_CORREO = %s, PER_DIRECCION = %s, PER_IDENTIFICACION = %s, PER_TELEFONO = %s WHERE PER_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("per_nombre", "per_seg_nombre", "per_pri_apellido", "per_seg_apellido", "per_correo", "per_direccion", "per_identificacion", "per_telefono", "per_id"))
    current_app.mysql.connection.commit()
    c.close()

    return "Persona actualizada correctamente"