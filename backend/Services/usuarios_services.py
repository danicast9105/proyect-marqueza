from flask import current_app
from Models.user import User

def servListUser():
    sql = "SELECT * FROM T_CLIENTE"
    # la siguiente linea es para ejecutar la consulta sql
    c   = current_app.mysql.connection.cursor() 
    c.execute(sql)
    # la siguiente linea es para obtener los resultados de la consulta sql
    data = c.fetchall()
    print(data)
    # u = []
    users_l =[ ]
    for u in data:
        users_l.append(User(u[0],u[1],u[2],u[3],u[4],u[5]).to_dic())

    print(users_l)
    # la siguiente linea es para cerrar la conexion a la base de datos
    c.close()
    return users_l


def addUser():
    pass

def upUser():
    pass

def delUser():
    pass

def searchByDoc(documento):
    pass
