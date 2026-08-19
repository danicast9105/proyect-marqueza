from Models.user import User

def servListUser():
    sql = "SELECT * FROM T_DETALLES_ETC"
    # la siguiente linea es para ejecutar la consulta sql
    c   = current_app.mysql.connection.cursor() 
    c.execute(sql)
    # la siguiente linea es para obtener los resultados de la consulta sql
    data = c.fetchall()
    print(data)
    # u = []
    Det_etc =[ ]
    for u in data:
        Det_etc.append(User(u[0],u[1],u[2],u[3],u[4],u[5]).to_dic())

    print(Det_etc)
    # la siguiente linea es para cerrar la conexion a la base de datos
    c.close()
    return Det_etc


def addUser():
    pass

def upUser():
    pass

def delUser():
    pass

def searchByDoc(documento):
    pass