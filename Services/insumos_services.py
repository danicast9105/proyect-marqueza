from flask import current_app
from Models.insumos import Insumos

def servListInsumos():

    sql = "SELECT * FROM T_INSUMOS"

    c   = current_app.mysql.connection.cursor() 
    c.execute(sql)
        
    data = c.fetchall()
    print(data)
        
    insumos_l =[ ]
    for u in data:
        insumos_l.append(Insumos(u[0],u[1],u[2],u[3],u[4],u[5],u[6],u[7],u[8],u[9]).to_dic())
    
    print(insumos_l)
    c.close()
    
    return insumos_l

def addInsumos():
    sql = "INSERT INTO T_INSUMOS (INS_UUID, INS_CODIGO, INS_NOMBRE, INS_CANTIDAD, INS_PRECIO, INS_ESTADO, INS_USUA_ID, INS_DET_ETC_ID, INS_PROV_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    c   = current_app.mysql.connection.cursor()
    c.execute(sql, ("ins_uuid", "ins_codigo, ins_nombre, ins_cantidad, ins_precio, ins_estado, ins_usua_id, ins_det_etc_id, ins_prov_id"))
    current_app.mysql.connection.commit()

    c.close()
    return "Insumo agregado correctamente"

def deleteInsumos():
    sql = "DELETE FROM T_INSUMOS WHERE INS_ID = %s"
    
    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("ins_id",))
    current_app.mysql.connection.commit()
    c.close()
    
    return "Insumo eliminado correctamente"
    
def updateInsumos():
    sql = "UPDATE T_INSUMOS SET INS_UUID = %s, INS_CODIGO = %s, INS_NOMBRE = %s, INS_CANTIDAD = %s, INS_PRECIO = %s, INS_ESTADO = %s, INS_USUA_ID = %s, INS_DET_ETC_ID = %s, INS_PROV_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("ins_uuid", "ins_codigo, ins_nombre, ins_cantidad, ins_precio, ins_estado, ins_usua_id, ins_det_etc_id, ins_prov_id"))
    current_app.mysql.connection.commit()
    c.close()

    return "Insumo actualizado correctamente"
    