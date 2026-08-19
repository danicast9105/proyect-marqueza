from Models.user import User

def servListUser():
    sql = "SELECT * FROM T_VENT_PROD"
    # la siguiente linea es para ejecutar la consulta sql
    c   = current_app.mysql.connection.cursor() 
    c.execute(sql)
    # la siguiente linea es para obtener los resultados de la consulta sql
    data = c.fetchall()
    print(data)
    # u = []
    Vent_Prod =[ ]
    for u in data:
        Vent_Prod.append(User(u[0],u[1],u[2],u[3],u[4],u[5]).to_dic())

    print(Vent_Prod)
    # la siguiente linea es para cerrar la conexion a la base de datos
    c.close()
    return Vent_Prod


def addUser():
    pass

def upUser():
    pass

def delUser():
    pass

def searchByDoc(documento):
    pass