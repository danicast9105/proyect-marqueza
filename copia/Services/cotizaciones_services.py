from flask import current_app
from Models.cotizaciones import Cotizaciones

def servListCotizaciones():
    sql = "SELECT * FROM T_COTIZACIONES"

    c   = current_app.mysql.connection.cursor() 
    c.execute(sql)
    
    data = c.fetchall()
    print(data)
    
    cotizaciones_l =[ ]
    for u in data:
        cotizaciones_l.append(Cotizaciones(u[0],u[1],u[2],u[3],u[4],u[5],u[6],u[7],u[8]).to_dic())

    print(cotizaciones_l)
    c.close()

    return cotizaciones_l

def addCotizaciones():
    sql = "INSERT INTO T_COTIZACIONES (COT_UUID, COT_PRO_CODIGO, COT_PRO_NOMBRE, COT_CANTIDAD, COT_PRECIO, COT_TOTAL_PAGAR, COT_USUA_ID, COT_CLI_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    c   = current_app.mysql.connection.cursor()
    c.execute(sql, ("cot_uuid", "cot_pro_codigo", "cot_pro_nombre", "cot_cantidad", "cot_precio", "cot_total_pagar", "cot_usua_id", "cot_cli_id"))
    current_app.mysql.connection.commit()

    c.close()
    return "Cotización agregada correctamente"

def deleteCotizaciones():
    sql = "DELETE FROM T_COTIZACIONES WHERE COT_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("cot_id",))
    current_app.mysql.connection.commit()
    c.close()

    return "Cotización eliminada correctamente"

def updateCotizaciones():
    sql = "UPDATE T_COTIZACIONES SET COT_PRO_CODIGO = %s, COT_PRO_NOMBRE = %s, COT_CANTIDAD = %s, COT_PRECIO = %s, COT_TOTAL_PAGAR = %s, COT_USUA_ID = %s, COT_CLI_ID = %s WHERE COT_ID = %s"

    c = current_app.mysql.connection.cursor()
    c.execute(sql, ("cot_pro_codigo", "cot_pro_nombre", "cot_cantidad", "cot_precio", "cot_total_pagar", "cot_usua_id", "cot_cli_id", "cot_id"))
    current_app.mysql.connection.commit()
    c.close()

    return "Cotización actualizada correctamente"